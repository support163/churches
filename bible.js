(function () {
  const form = document.getElementById("bible-form");
  const input = document.getElementById("bible-input");
  const body = document.getElementById("bible-body");

  let messagesEl = null;

  function ensureMessagesContainer() {
    if (messagesEl && messagesEl.isConnected) return messagesEl;
    body.innerHTML = "";
    messagesEl = document.createElement("div");
    messagesEl.className = "messages";
    body.appendChild(messagesEl);
    return messagesEl;
  }

  function scrollToBottom() {
    body.scrollTop = body.scrollHeight;
  }

  function addUserMessage(text) {
    const el = ensureMessagesContainer();
    const div = document.createElement("div");
    div.className = "msg user";
    div.textContent = text;
    el.appendChild(div);
    scrollToBottom();
  }

  function addTyping() {
    const el = ensureMessagesContainer();
    const div = document.createElement("div");
    div.className = "typing";
    div.textContent = "Looking up passage…";
    el.appendChild(div);
    scrollToBottom();
    return div;
  }

  function addErrorMessage(text) {
    const el = ensureMessagesContainer();
    const div = document.createElement("div");
    div.className = "msg bot error";
    div.textContent = text;
    el.appendChild(div);
    scrollToBottom();
  }

  function addPassageMessage(data) {
    const el = ensureMessagesContainer();
    const div = document.createElement("div");
    div.className = "msg bot";

    const ref = document.createElement("span");
    ref.className = "ref";
    ref.textContent = data.reference;
    div.appendChild(ref);

    if (Array.isArray(data.verses) && data.verses.length > 1) {
      data.verses.forEach((v) => {
        const num = document.createElement("span");
        num.className = "verse-num";
        num.textContent = v.verse;
        div.appendChild(num);
        div.appendChild(document.createTextNode(v.text.trim() + " "));
      });
    } else {
      div.appendChild(document.createTextNode(data.text.trim()));
    }

    if (data.translation_name || data.translation_id) {
      const t = document.createElement("span");
      t.className = "translation";
      t.textContent =
        "— " + (data.translation_name || data.translation_id.toUpperCase());
      div.appendChild(t);
    }

    el.appendChild(div);
    scrollToBottom();
  }

  async function lookup(reference) {
    const url =
      "https://bible-api.com/" + encodeURIComponent(reference) + "?translation=web";
    const res = await fetch(url);
    if (!res.ok) {
      throw new Error("Reference not found.");
    }
    const data = await res.json();
    if (data.error) {
      throw new Error(data.error);
    }
    return data;
  }

  async function handleSubmit(reference) {
    if (!reference) return;
    addUserMessage(reference);
    const typing = addTyping();
    try {
      const data = await lookup(reference);
      typing.remove();
      addPassageMessage(data);
    } catch (err) {
      typing.remove();
      addErrorMessage(
        'Sorry, I couldn\'t find "' +
          reference +
          '". Try a reference like "John 3:16" or "Psalm 23".'
      );
    }
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const value = input.value.trim();
    if (!value) return;
    input.value = "";
    handleSubmit(value);
  });

  document.querySelectorAll(".chip[data-ref]").forEach((btn) => {
    btn.addEventListener("click", () => {
      handleSubmit(btn.getAttribute("data-ref"));
    });
  });
})();
