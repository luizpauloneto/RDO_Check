// ==========================================================
// RDO CHECK
// app/static/js/index.js
// ==========================================================

class IndexController {

    constructor() {

        this.form = document.getElementById("uploadForm");
        this.fileInput = document.getElementById("pdf");
        this.uploadArea = document.querySelector(".upload-area");
        this.button = document.getElementById("btnUpload");

        this.currentJob = null;

        this.initialize();

    }

    //==========================================================

    initialize() {

        this.initializeDragDrop();

        this.initializeForm();

        this.loadRecentJobs();

        this.startHeartbeat();

    }

    //==========================================================

    initializeDragDrop() {

        if (!this.uploadArea)
            return;

        this.uploadArea.addEventListener("click", () => {

            this.fileInput.click();

        });

        this.uploadArea.addEventListener("dragover", e => {

            e.preventDefault();

            this.uploadArea.classList.add("drag");

        });

        this.uploadArea.addEventListener("dragleave", () => {

            this.uploadArea.classList.remove("drag");

        });

        this.uploadArea.addEventListener("drop", e => {

            e.preventDefault();

            this.uploadArea.classList.remove("drag");

            if (!e.dataTransfer.files.length)
                return;

            this.fileInput.files = e.dataTransfer.files;

            this.showSelectedFile();

        });

        this.fileInput.addEventListener("change", () => {

            this.showSelectedFile();

        });

    }

    //==========================================================

    showSelectedFile() {

        if (!this.fileInput.files.length)
            return;

        const file = this.fileInput.files[0];

        this.uploadArea.querySelector("p").innerHTML =

            "<strong>" +

            file.name +

            "</strong><br><br>" +

            (file.size / 1024 / 1024).toFixed(2) +

            " MB";

    }

    //==========================================================

    initializeForm() {

        if (!this.form)
            return;

        this.form.addEventListener(

            "submit",

            async (event) => {

                event.preventDefault();

                await this.upload();

            }

        );

    }

    //==========================================================

    async upload() {

        if (!this.fileInput.files.length) {

            this.toast(

                "Selecione um PDF.",

                "warning"

            );

            return;

        }

        this.button.disabled = true;

        this.button.innerHTML = "Enviando...";

        const formData = new FormData();

        formData.append(

            "file",

            this.fileInput.files[0]

        );

        try {

            const response = await fetch(

                "/api/upload",

                {

                    method: "POST",

                    body: formData

                }

            );

            if (!response.ok) {

                throw new Error(

                    "Falha no upload."

                );

            }

            const data = await response.json();

            this.currentJob =

                data.job_id;

            this.toast(

                "Documento enviado.",

                "success"

            );

            this.monitorJob();

        }

        catch (ex) {

            console.error(ex);

            this.toast(

                ex.message,

                "error"

            );

            this.button.disabled = false;

            this.button.innerHTML =

                "Processar Documento";

        }

    }

    //==========================================================

    async monitorJob() {

        if (!this.currentJob)
            return;

        const timer = setInterval(

            async () => {

                try {

                    const response = await fetch(

                        "/api/jobs/" +

                        this.currentJob

                    );

                    if (!response.ok)
                        return;

                    const job =

                        await response.json();

                    if (

                        job.status === "finished"

                    ) {

                        clearInterval(timer);

                        location.href =

                            "/processamento?job=" +

                            this.currentJob;

                    }

                    if (

                        job.status === "error"

                    ) {

                        clearInterval(timer);

                        this.toast(

                            "Erro no processamento.",

                            "error"

                        );

                    }

                }

                catch (ex) {

                    console.error(ex);

                }

            },

            1000

        );

    }

    //==========================================================

    async loadRecentJobs() {

        try {

            const response = await fetch(

                "/api/jobs"

            );

            if (!response.ok)
                return;

            const jobs =

                await response.json();

            const body =

                document.querySelector(

                    "#recentJobs tbody"

                );

            if (!body)
                return;

            body.innerHTML = "";

            jobs.forEach(job => {

                const tr =

                    document.createElement(

                        "tr"

                    );

                tr.innerHTML =

                    `
                    <td>${job.id}</td>
                    <td>${job.filename}</td>
                    <td>${job.status}</td>
                    <td>${job.company || "-"}</td>
                    <td>${job.date || "-"}</td>
                    `;

                tr.onclick = () => {

                    location.href =

                        "/processamento?job=" +

                        job.id;

                };

                body.appendChild(tr);

            });

        }

        catch (ex) {

            console.error(ex);

        }

    }

    //==========================================================

    startHeartbeat() {

        setInterval(

            async () => {

                try {

                    const response = await fetch(

                        "/health"

                    );

                    const data =

                        await response.json();

                    const obj =

                        document.getElementById(

                            "serverStatus"

                        );

                    if (obj) {

                        obj.innerHTML =

                            data.status;

                    }

                }

                catch {

                    const obj =

                        document.getElementById(

                            "serverStatus"

                        );

                    if (obj) {

                        obj.innerHTML =

                            "Offline";

                    }

                }

            },

            5000

        );

    }

    //==========================================================

    toast(message, type = "info") {

        if (

            window.RDO &&

            window.RDO.toast

        ) {

            window.RDO.toast(

                message,

                type

            );

            return;

        }

        console.log(message);

    }

}

//==========================================================

window.addEventListener(

    "DOMContentLoaded",

    () => {

        window.index =

            new IndexController();

    }

);