/*
** JavaScript for Powerwiki show page
*/

import { addCtrlKeyListener } from "../lib/keys.js";

export const setup = () => {
  const formShowEdit = document.getElementById('powerwiki__page__edit');
  if (!formShowEdit) {
    return;
  }

  addCtrlKeyListener('e', e => {
    formShowEdit.click()
  });
};
