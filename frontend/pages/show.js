/*
** JavaScript for Powerwiki show page
*/

import { addCtrlKeyListener } from "../lib/keys.js";


let lastTitleIndex = 0;

class Title {
  constructor(el) {
    this.el = el;
    el._powerwikiTitle = this;
    this.text = el.innerText;
    this.id = this.text.toLowerCase().split(" ").join('-');
    this.level = parseInt(el.tagName[1], 10);
    this.children = [];
    this.index = ++lastTitleIndex;
    el.setAttribute('id', this.id)

    this.sidebarEl = document.createElement("a");
    this.sidebarEl.href=`#${this.id}`;
    this.sidebarEl.innerText = this.text;
  }
}


class TitleSidebar {
  constructor(contentEl, sidebarEl) {
    this.contentEl = contentEl;
    this.sidebarEl = sidebarEl;
    this.generateSidebar();
    this.observe();
  }
  generateSidebar() {
    const titleEls = this.contentEl.querySelectorAll("h1, h2, h3, h4, h5, h6");
    this.titles = [];

    // Create a stack to keep track of the parent nodes
    const stack = [{ level: 0, node: document.createElement("ul") }];

    // Iterate through the heading elements
    titleEls.forEach((el) => {
      const title = new Title(el);
      this.titles.push(title);

      const li = document.createElement("li");
      li.appendChild(title.sidebarEl);

      // Remove nodes from the stack that have a level greater than the current title level
      while (stack.length > 1 && stack[stack.length - 1].level >= title.level) {
        if (stack[stack.length - 1].node.children.length == 0) {
          stack[stack.length - 1].node.remove();
        }
        stack.pop();
      }

      // Add the li element to the parent node
      stack[stack.length - 1].node.appendChild(li);

      // Create a new parent node and add it to the stack
      const parent = { level: title.level, node: document.createElement("ul") };
      stack[stack.length - 1].node.lastElementChild.appendChild(parent.node);
      stack.push(parent);
    });

    // Get the root node from the stack and append it to the document body
    const root = stack[0].node;
    this.sidebarEl.appendChild(root);
  }

  observe() {
    // Create an intersection observer
    let currentSelection = null;
    let visible = [];

    const observer = new IntersectionObserver(changes => {
      // Find which are visible
      changes.forEach(change => {
        // Check if the header element is intersecting with the viewport
        const title = change.target._powerwikiTitle;
        if (!change.isIntersecting) {
          if (visible.length) {
            visible = visible.filter(obj => obj != title);
          }
          return;

        } else {
          visible.push(title);
        }
      });

      // Highest on page
      if (!visible.length) {
        // Nothing on page, stick with previous
        return;
      }
      let newSelection = visible.reduce((min, obj) => {
        return obj.index < min.index ? obj : min;
      });

      if (newSelection == currentSelection) {
        return;
      }

      // Log the header element to the console
      if (currentSelection) {
        currentSelection.sidebarEl.classList.remove('selected');
      }
      currentSelection = newSelection;
      currentSelection.sidebarEl.classList.add('selected');

      // Update URL to fragment
      const url = window.location.href;
      const urlParts = url.split("#");
      const newUrl = `${url.split('#')[0]}#${currentSelection.id}`;
      window.history.replaceState(null, null, newUrl);
    });

    // Observe each header element
    this.titles.forEach((title) => {
      observer.observe(title.el);
    });
  }
}


export const setup = () => {
  const formShowEdit = document.getElementById('powerwiki__page__edit');
  if (!formShowEdit) {
    return;
  }

  addCtrlKeyListener('e', e => {
    formShowEdit.click()
  });

  new TitleSidebar(
    document.querySelector('.powerwiki__page'),
    document.querySelector('.powerwiki__sidebar'),
  );
};
