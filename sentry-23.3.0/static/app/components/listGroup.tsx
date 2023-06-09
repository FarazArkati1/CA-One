import styled from '@emotion/styled';

import {space} from 'sentry/styles/space';

type ListGroupProps = {
  striped?: boolean;
};

type ListGroupItemProps = {
  centered?: boolean;
};

const ListGroupItem = styled('li')<ListGroupItemProps>`
  position: relative;
  display: block;
  min-height: 36px;
  border: 1px solid ${p => p.theme.border};

  padding: ${space(0.5)} ${space(1.5)};

  margin-bottom: -1px;
  ${p => (p.centered ? 'text-align: center;' : '')}

  &:first-child {
    border-top-left-radius: ${p => p.theme.borderRadius};
    border-top-right-radius: ${p => p.theme.borderRadius};
  }
  &:last-child {
    border-bottom-left-radius: ${p => p.theme.borderRadius};
    border-bottom-right-radius: ${p => p.theme.borderRadius};
  }
`;

const ListGroup = styled('ul')<ListGroupProps>`
  box-shadow: 0 1px 0px rgba(0, 0, 0, 0.03);
  background: ${p => p.theme.background};
  padding: 0;
  margin: 0;

  ${p =>
    p.striped
      ? `
    & > li:nth-child(odd) {
      background: ${p.theme.backgroundSecondary};
    }
  `
      : ''}
`;

export {ListGroup, ListGroupItem};
