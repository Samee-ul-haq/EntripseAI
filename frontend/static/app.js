const state = {
  user: null,
  workspaces: [],
  workspaceId: null,
  conversations: [],
  activeConversation: null,
  documents: [],
};

const qs = (selector) => document.querySelector(selector);

function getCookie(name) {
  return document.cookie
    .split(";")
    .map((cookie) => cookie.trim())
    .find((cookie) => cookie.startsWith(`${name}=`))
    ?.split("=")[1];
}

async function api(path, options = {}) {
  const headers = {
    ...(options.body instanceof FormData ? {} : { "Content-Type": "application/json" }),
    "X-CSRFToken": getCookie("csrftoken") || "",
    ...options.headers,
  };
  const response = await fetch(path, {
    credentials: "same-origin",
    ...options,
    headers,
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: response.statusText }));
    throw new Error(Object.values(error).flat().join(" ") || "Request failed");
  }
  if (response.status === 204) {
    return null;
  }
  return response.json();
}

function render() {
  const signedIn = Boolean(state.user);
  qs("#auth-panel").classList.toggle("hidden", signedIn);
  qs("#workspace-panel").classList.toggle("hidden", !signedIn);
  qs("#conversation-form").classList.toggle("hidden", !state.workspaceId);
  qs("#document-form").classList.toggle("hidden", !state.workspaceId);
  qs("#current-user").textContent = signedIn ? state.user.username : "Not signed in";

  const activeWorkspace = state.workspaces.find((workspace) => String(workspace.id) === String(state.workspaceId));
  qs("#workspace-title").textContent = activeWorkspace ? activeWorkspace.name : "Welcome";
  qs("#current-workspace").textContent = activeWorkspace ? activeWorkspace.name : "None";
  qs("#status-text").textContent = signedIn
    ? "Conversations and documents are isolated by workspace."
    : "Register or login to begin.";

  qs("#workspace-select").innerHTML = state.workspaces
    .map((workspace) => `<option value="${workspace.id}">${workspace.name}</option>`)
    .join("");
  qs("#workspace-select").value = state.workspaceId || "";

  qs("#conversation-list").innerHTML = state.conversations.length
    ? state.conversations
        .map(
          (conversation) => `
            <div class="item">
              <button type="button" data-conversation="${conversation.id}">
                <strong>${conversation.title || `Conversation ${conversation.id}`}</strong>
                <div class="meta">${conversation.model} · ${conversation.message_count || 0} messages</div>
              </button>
            </div>
          `,
        )
        .join("")
    : '<div class="empty">No conversations yet.</div>';

  const messages = state.activeConversation?.messages || [];
  qs("#messages").innerHTML = messages.length
    ? messages
        .map(
          (message) => `
            <article class="message">
              <strong>${message.role}</strong>
              <div>${message.content.replaceAll("<", "&lt;").replaceAll(">", "&gt;")}</div>
              <div class="meta">${message.model || "manual"} ${message.latency_ms ? `· ${message.latency_ms} ms` : ""}</div>
            </article>
          `,
        )
        .join("")
    : '<div class="empty">Save a prompt and response to build conversation history.</div>';

  qs("#document-list").innerHTML = state.documents.length
    ? state.documents
        .map(
          (document) => `
            <div class="item">
              <strong>${document.filename}</strong>
              <div class="meta">${Math.ceil(document.size / 1024)} KB · ${document.content_type || "file"}</div>
            </div>
          `,
        )
        .join("")
    : '<div class="empty">No documents uploaded.</div>';
}

async function refreshWorkspaces() {
  const data = await api("/api/workspaces/");
  state.workspaces = data.results || data;
  state.workspaceId = state.workspaceId || state.workspaces[0]?.id || null;
  render();
  await Promise.all([refreshConversations(), refreshDocuments()]);
}

async function refreshConversations() {
  if (!state.workspaceId) {
    state.conversations = [];
    state.activeConversation = null;
    render();
    return;
  }
  const data = await api("/api/conversations/");
  state.conversations = (data.results || data).filter(
    (conversation) => String(conversation.workspace) === String(state.workspaceId),
  );
  state.activeConversation = state.conversations[0] || null;
  render();
}

async function refreshDocuments() {
  if (!state.workspaceId) {
    state.documents = [];
    render();
    return;
  }
  const data = await api("/api/documents/");
  state.documents = (data.results || data).filter(
    (document) => String(document.workspace) === String(state.workspaceId),
  );
  render();
}

async function loadMe() {
  try {
    state.user = await api("/api/auth/me/");
    await refreshWorkspaces();
  } catch {
    state.user = null;
    render();
  }
}

qs("#login-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(event.currentTarget));
  state.user = await api("/api/auth/login/", {
    method: "POST",
    body: JSON.stringify(data),
  });
  event.currentTarget.reset();
  await refreshWorkspaces();
});

qs("#register-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(event.currentTarget));
  state.user = await api("/api/auth/register/", {
    method: "POST",
    body: JSON.stringify(data),
  });
  event.currentTarget.reset();
  await refreshWorkspaces();
});

qs("#logout-button").addEventListener("click", async () => {
  await api("/api/auth/logout/", { method: "POST" });
  state.user = null;
  state.workspaces = [];
  state.workspaceId = null;
  state.conversations = [];
  state.documents = [];
  state.activeConversation = null;
  render();
});

qs("#workspace-select").addEventListener("change", async (event) => {
  state.workspaceId = event.currentTarget.value;
  await Promise.all([refreshConversations(), refreshDocuments()]);
});

qs("#workspace-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(event.currentTarget));
  const workspace = await api("/api/workspaces/", {
    method: "POST",
    body: JSON.stringify(data),
  });
  state.workspaceId = workspace.id;
  event.currentTarget.reset();
  await refreshWorkspaces();
});

qs("#conversation-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = new FormData(event.currentTarget);
  const payload = Object.fromEntries(formData);
  payload.workspace = state.workspaceId;
  payload.title = payload.prompt.slice(0, 80);
  if (!payload.latency_ms) {
    payload.latency_ms = null;
  }
  const conversation = await api("/api/conversations/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  state.activeConversation = conversation;
  event.currentTarget.reset();
  event.currentTarget.model.value = "manual";
  await refreshConversations();
});

qs("#document-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = new FormData(event.currentTarget);
  formData.append("workspace", state.workspaceId);
  await api("/api/documents/", {
    method: "POST",
    body: formData,
  });
  event.currentTarget.reset();
  await refreshDocuments();
});

qs("#conversation-list").addEventListener("click", (event) => {
  const button = event.target.closest("[data-conversation]");
  if (!button) {
    return;
  }
  state.activeConversation = state.conversations.find(
    (conversation) => String(conversation.id) === String(button.dataset.conversation),
  );
  render();
});

loadMe();
