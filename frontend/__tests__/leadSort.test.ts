import { describe, expect, it } from 'vitest';

function sortByStatus(a: any, b: any) {
  return a.status.localeCompare(b.status);
}

describe('lead sort', () => {
  it('orders by status alphabetically', () => {
    const arr = [{ status: 'WON' }, { status: 'NEW' }];
    expect(arr.sort(sortByStatus)[0].status).toBe('NEW');
  });
}); 