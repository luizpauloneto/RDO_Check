// =====================================================
// RDO Check
// app/static/js/app.js
// =====================================================

class RDOApp {

    constructor() {

        this.sidebarCollapsed = false;
        this.socket = null;

        this.init();

    }

    init() {

        console.log("RDO Check iniciado.");

        this.initSidebar();

        this.connectWebSocket();

        this.registerEvents();

    }

    // =====================================================
    // Sidebar
    // =====================================================

    initSidebar() {

        const sidebar = document.querySelector(".sidebar");
        const page = document.querySelector(".page");

        if (!sidebar || !page)
            return;

        let button = document.getElementById("sidebar-toggle");

        if (!button) {

            button = document.createElement("button");

            button.id = "sidebar-toggle";

            button.innerHTML = "☰";

            button.className = "sidebar-button";

            sidebar.prepend(button);

        }

        button.onclick = () => {

            this.sidebarCollapsed = !this.sidebarCollapsed;

            if (this.sidebarCollapsed) {

                sidebar.style.width = "72px";

                page.style.marginLeft = "72px";

                page.style.width = "calc(100% - 72px)";

            }

            else {

                sidebar.style.width = "250px";

                page.style.marginLeft = "250px";

                page.style.width = "calc(100% - 250px)";

            }

        };

    }

    // =====================================================
    // WebSocket
    // =====================================================

    connectWebSocket() {

        const protocol = location.protocol === "https:"
            ? "wss"
            : "ws";

        const url = `${protocol}://${location.host}/ws`;

        try {

            this.socket = new WebSocket(url);

            this.socket.onopen = () => {

                this.toast("WebSocket conectado");

            };

            this.socket.onclose = () => {

                this.toast("Conexão perdida");

                setTimeout(() => {

                    this.connectWebSocket();

                }, 5000);

            };

            this.socket.onerror = (err) => {

                console.error(err);

            };

            this.socket.onmessage = (event) => {

                this.handleMessage(event.data);

            };

        }

        catch (e) {

            console.error(e);

        }

    }

    // =====================================================
    // Mensagens
    // =====================================================

    handleMessage(message) {

        try {

            const data = JSON.parse(message);

            if (data.progress !== undefined) {

                this.updateProgress(data.progress);

            }

            if (data.status) {

                const obj = document.getElementById("job-status");

                if (obj)
                    obj.innerText = data.status;

            }

            if (data.toast) {

                this.toast(data.toast);

            }

        }

        catch {

            console.log(message);

        }

    }

    // =====================================================
    // Progress
    // =====================================================

    updateProgress(value) {

        const bar = document.querySelector(".progress-bar");

        if (!bar)
            return;

        bar.style.width = value + "%";

    }

    // =====================================================
    // Loader
    // =====================================================

    showLoader() {

        document.body.classList.add("loading");

    }

    hideLoader() {

        document.body.classList.remove("loading");

    }

    // =====================================================
    // Toast
    // =====================================================

    toast(text) {

        let container = document.getElementById("toast-container");

        if (!container) {

            container = document.createElement("div");

            container.id = "toast-container";

            container.style.position = "fixed";

            container.style.right = "20px";

            container.style.top = "20px";

            container.style.zIndex = "99999";

            document.body.appendChild(container);

        }

        const toast = document.createElement("div");

        toast.className = "toast";

        toast.innerText = text;

        toast.style.background = "#1e293b";

        toast.style.color = "#FFF";

        toast.style.padding = "12px";

        toast.style.marginBottom = "10px";

        toast.style.borderRadius = "8px";

        toast.style.borderLeft = "4px solid #2563eb";

        toast.style.boxShadow = "0 0 10px rgba(0,0,0,.3)";

        container.appendChild(toast);

        setTimeout(() => {

            toast.remove();

        }, 3500);

    }

    // =====================================================
    // Eventos globais
    // =====================================================

    registerEvents() {

        window.addEventListener("resize", () => {

            console.log("Resize");

        });

    }

}

// =====================================================

window.addEventListener(

    "DOMContentLoaded",

    () => {

        window.RDO = new RDOApp();

    }

);