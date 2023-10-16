from celery import shared_task
from .models import *
def expense_split_check(paid_by,split_type,split_details,amount):
    no_of_people=len(split_details)
    people=list(split_details.keys())
    values=list(split_details.values())
    
    if split_type == "EQL":
        for i in range (no_of_people):
            split_details[people[i]] = -round(amount/no_of_people,2)


    elif split_type == "UEQ":
        if amount != sum(values):
            return False
        else:
            for i in range (no_of_people):
                split_details[people[i]] = -values[i]


    elif split_type == "PER":
        if sum(values) != 100:
            return False
        else:
            for i in range (no_of_people):
                split_details[people[i]] = -amount*values[i]/100
            
        
    split_details[paid_by] = amount + split_details[paid_by]
    return split_details


def seperating_people(people_dict):
    owers=[]
    borrowers=[]

    for x in people_dict.keys():
        temp=people_dict[x]
        if temp>0:
            owers.append(x)
        if temp<0:
            borrowers.append(x)
    return owers,borrowers


@shared_task(bind=True)
def user_balance_sheet(request,condensed_transactions,group_id):
    
    for i in condensed_transactions:
        if condensed_transactions[i]>0:
            user=UserProfile.objects.get(id=int(i))
            
            user.expense_map[group_id]={"owed":condensed_transactions[i],"borrowed":0}
            user.save(update_fields=["expense_map"]) 

        elif condensed_transactions[i]<0:
            user=UserProfile.objects.get(id=int(i))
            user.expense_map[group_id]={"owed":0,"borrowed":abs(condensed_transactions[i])}
            user.save(update_fields=["expense_map"])

 
    print("User Balance Sheet Updated")


@shared_task(bind=True)
def group_balance_sheet(request,group_id):
    group=Group.objects.get(id=group_id)
   
    expenses=Expense.objects.filter(group=group.id)
    members=[str(i.id) for i in (group.members.all())]
    expenses=[i.split_details for i in expenses]
    
    

    condensed_transactions={m:0 for m in members}
    
    for i in members:
       
        for j in expenses:
            try:
                condensed_transactions[i]+=j[i]
            except:
                pass
    
    user_balance_sheet.delay(condensed_transactions,group_id)
    
    owers,borrowers=seperating_people(condensed_transactions)
    ower_p,borrower_p=0,0
    final=[]
    
    while ower_p<len(owers) and borrower_p<len(borrowers):
        if (condensed_transactions[borrowers[borrower_p]])!=0 and condensed_transactions[owers[ower_p]]!=0:
            
            if abs(condensed_transactions[borrowers[borrower_p]])>abs(condensed_transactions[owers[ower_p]]):

                final.append([str(borrowers[borrower_p]),str(owers[ower_p]),float(abs(condensed_transactions[owers[ower_p]]))])
                condensed_transactions[borrowers[borrower_p]]+=condensed_transactions[owers[ower_p]]
                condensed_transactions[owers[ower_p]]=0
                
                ower_p+=1
            
            elif abs(condensed_transactions[borrowers[borrower_p]])<abs(condensed_transactions[owers[ower_p]]):
                final.append([str(borrowers[borrower_p]),str(owers[ower_p]),float(abs(condensed_transactions[borrowers[borrower_p]]))])
                condensed_transactions[owers[ower_p]]+=condensed_transactions[borrowers[borrower_p]]
                condensed_transactions[borrowers[borrower_p]]=0
                borrower_p+=1
                
            
            elif abs(condensed_transactions[borrowers[borrower_p]])==abs(condensed_transactions[owers[ower_p]]):
                final.append([str(borrowers[borrower_p]),str(owers[ower_p]),float(abs(condensed_transactions[borrowers[borrower_p]]))])
                condensed_transactions[owers[ower_p]]=0
                condensed_transactions[borrowers[borrower_p]]=0
                borrower_p+=1
                ower_p+=1
                
        else:
            if condensed_transactions[borrowers[borrower_p]]==0:
                borrower_p+=1
            if condensed_transactions[owers[ower_p]]==0:
                ower_p+=1
    
    exp=[]

    for i in final:
        exp.append(str(i[0])+" owes "+str(i[1])+" Rs "+str(i[2]))

    print(exp)
    group.expense_map={"expenses":exp}
    group.save(update_fields=["expense_map"]) 


    print("done")



