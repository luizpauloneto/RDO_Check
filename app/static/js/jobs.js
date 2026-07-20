// =====================================================
// RDO Check
// app/static/js/jobs.js
// =====================================================

class JobsController {

    constructor() {
        this.table = document.getElementById("jobsGrid");
        this.search = document.getElementById("searchText");
        this.status = document.getElementById("statusFilter");

        this.jobs = [];
        this.filtered = [];
        this.page = 1;
        this.pageSize = 20;

        this.initialize();
    }

    initialize() {
        this.bindEvents();
        this.loadMock();
        this.render();
    }

    bindEvents() {
        const btn = document.getElementById("btnSearch");
        if (btn) {
            btn.addEventListener("click", () => this.filter());
        }

        const refresh = document.getElementById("btnRefresh");
        if (refresh) {
            refresh.addEventListener("click", () => this.refresh());
        }
    }

    refresh() {
        console.log("Atualizando lista...");
        this.render();
    }

    loadMock() {
        for (let i = 1; i <= 50; i++) {
            this.jobs.push({
                id: "JOB-" + String(i).padStart(5, "0"),
                file: `RDO_${i}.pdf`,
                company: "CMOC",
                pages: Math.floor(Math.random() * 40) + 1,
                status: i % 5 === 0 ? "Erro" : (i % 2 === 0 ? "Processando" : "Finalizado"),
                start: "13/07/2026 08:00",
                elapsed: "00:02:15",
                confidence: (95 + Math.random() * 5).toFixed(1)
            });
        }

        this.filtered = [...this.jobs];
    }

    filter() {
        const text = (this.search?.value || "").toLowerCase();
        const status = this.status?.value || "";

        this.filtered = this.jobs.filter(j => {
            const okText =
                j.file.toLowerCase().includes(text) ||
                j.id.toLowerCase().includes(text);

            const okStatus =
                status === "" || j.status === status;

            return okText && okStatus;
        });

        this.page = 1;
        this.render();
    }

    render() {
        if (!this.table) return;

        const body = this.table.querySelector("tbody");
        body.innerHTML = "";

        const start = (this.page - 1) * this.pageSize;
        const end = start + this.pageSize;

        this.filtered.slice(start, end).forEach(job => {

            const tr = document.createElement("tr");

            tr.innerHTML = `
                <td>${job.id}</td>
                <td>${job.file}</td>
                <td>${job.company}</td>
                <td>${job.pages}</td>
                <td>${job.status}</td>
                <td>${job.start}</td>
                <td>${job.elapsed}</td>
                <td>${job.confidence}%</td>
                <td>
                    <button onclick="jobs.open('${job.id}')">Abrir</button>
                </td>`;

            body.appendChild(tr);
        });

        document.getElementById("totalJobs").textContent = this.jobs.length;
        document.getElementById("processingJobs").textContent =
            this.jobs.filter(x => x.status === "Processando").length;
        document.getElementById("finishedJobs").textContent =
            this.jobs.filter(x => x.status === "Finalizado").length;
        document.getElementById("errorJobs").textContent =
            this.jobs.filter(x => x.status === "Erro").length;
    }

    open(id) {
        console.log("Abrindo Job:", id);
    }
}

window.addEventListener("DOMContentLoaded", () => {
    window.jobs = new JobsController();
});
