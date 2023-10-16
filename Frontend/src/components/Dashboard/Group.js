import React, { Fragment } from 'react';
import Group from '../Forms/Groups';
import GroupsList from '../Lists/GroupsList';

export default function Groups() {
  return (
    <Fragment>
      <Group />
      <GroupsList />
    </Fragment>
  );
}