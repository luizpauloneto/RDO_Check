// =====================================================
// RDO Check
// app/static/js/dashboard.js
// =====================================================

class DashboardController {

    constructor() {
        this.jobsTable = document.getElementById("jobsTable");
        this.queueTable = document.getElementById("queueTable");
        this.logs = document.getElementById("liveLogs");
        this.init();
    }

    init() {
        console.log("Dashboard inicializado");
        this.mockRefresh();
    }

    updateCards(data) {
        this.set("jobsToday", data.jobs_today);
        this.set("jobsRunning", data.running);
        this.set("jobsFinished", data.finished);
        this.set("jobsError", data.errors);
        this.set("employees", data.employees);
        this.set("activities", data.activities);
        this.set("photos", data.photos);
        this.set("confidence", (data.confidence ?? 0) + " %");
    }

    updateGPU(data) {
        this.set("gpuName", data.name);
        this.set("gpuMemory", data.memory);
        this.set("gpuUsage", data.usage);
        this.set("gpuTemp", data.temperature);
        this.set("modelName", data.model);
    }

    updateProcessing(data) {
        this.set("currentFile", data.file);
        this.set("currentPage", data.page);
        this.set("currentStatus", data.status);
        this.set("elapsed", data.elapsed);

        const bar = document.getElementById("processingBar");
        if (bar) bar.style.width = (data.progress || 0) + "%";
    }

    updateQueue(items) {
        if (!this.queueTable) return;
        const body = this.queueTable.querySelector("tbody");
        body.innerHTML = "";
        items.forEach(i => {
            const tr = document.createElement("tr");
            tr.innerHTML = `<td>${i.file}</td><td>${i.pages}</td><td>${i.status}</td><td>${i.progress}%</td>`;
            body.appendChild(tr);
        });
    }

    updateJobs(items) {
        if (!this.jobsTable) return;
        const body = this.jobsTable.querySelector("tbody");
        body.innerHTML = "";
        items.forEach(i => {
            const tr = document.createElement("tr");
            tr.innerHTML = `<td>${i.id}</td><td>${i.company}</td><td>${i.date}</td><td>${i.status}</td><td>${i.time}</td><td>${i.confidence}%</td>`;
            body.appendChild(tr);
        });
    }

    addLog(text, level="info") {
        if (!this.logs) return;
        const div = document.createElement("div");
        div.className = level;
        div.textContent = "[" + new Date().toLocaleTimeString() + "] " + text;
        this.logs.prepend(div);
    }

    set(id, value) {
        const obj = document.getElementById(id);
        if (obj) obj.textContent = value;
    }

    mockRefresh() {
        this.updateCards({
            jobs_today:18,
            running:2,
            finished:16,
            errors:0,
            employees:143,
            activities:52,
            photos:38,
            confidence:98.4
        });

        this.updateGPU({
            name:"RTX 2000 Ada",
            memory:"7.2 / 16 GB",
            usage:"91 %",
            temperature:"54 °C",
            model:"Qwen2.5-VL"
        });

        this.updateProcessing({
            file:"RDO_TESTE.pdf",
            page:"3 / 12",
            status:"Extraindo colaboradores",
            elapsed:"00:02:14",
            progress:34
        });

        this.addLog("Dashboard carregado.");
    }
}

window.addEventListener("DOMContentLoaded", () => {
    window.dashboard = new DashboardController();
});
