/*
** JavaScript for Powerwiki edit page
*/

import CodeMirror from 'codemirror/lib/codemirror.js';
import "codemirror/lib/codemirror.css";
import "codemirror/mode/rst/rst";
import "codemirror/mode/markdown/markdown";

import { addCtrlKeyListener } from "../lib/keys.js";


// Map of Powerwiki markup engine to CodeMirror mode
const markupEngineToCodeMirror = {
  'powerwiki.markup.rest.RestructuredText': 'rst',
  'powerwiki.markup.md.Markdown': 'markdown',
};

export const setup = () => {
  const formEditSave = document.getElementById('powerwiki__form-edit__save');
  if (!formEditSave) {
    return;
  }

  const formMarkupEngine = document.querySelector(
    '.powerwiki__form-edit select[name="markup_engine"]'
  )
  const formContent = document.querySelector(
    '.powerwiki__form-edit__content textarea[name="content"]'
  );

  // Key management
  const setupKeys = () => {
    if (!formEditSave) {
      return;
    }
    addCtrlKeyListener('s', e => {
      formEditSave.click()
    });
  };

  // Content editor
  let editor;
  const initEditor = () => {
    // Turn off any existing editor
    if (editor) {
      editor.toTextArea();
    }

    // Add new editor
    const engine = formMarkupEngine.value;
    let mode = null;
    if (engine in markupEngineToCodeMirror) {
      mode = markupEngineToCodeMirror[engine];
    }
    editor = CodeMirror.fromTextArea(formContent, {
      mode: mode,
    });
  };
  formMarkupEngine.addEventListener("change", initEditor);

  setupKeys();
  initEditor();
};
