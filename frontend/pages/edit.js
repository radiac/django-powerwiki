/*
** JavaScript for Powerwiki edit page
*/

import { addCtrlKeyListener } from "../lib/keys.js";

export const setup = () => {
  const formEditSave = document.getElementById('powerwiki__form-edit__save');
  if (!formEditSave) {
    return;
  }

  addCtrlKeyListener('s', e => {
    formEditSave.click()
  });
};
