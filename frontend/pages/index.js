import { setup as setupShow } from "./show.js";
import { setup as setupEdit } from "./edit.js";


export const setup = () => {
  setupShow();
  setupEdit();
};
