/**
 * ==========================================================
 * processamento.js
 * RDO Check AI
 * ProcessingController v5
 * ==========================================================
 */

class ProcessingController {

    constructor() {

        // --------------------------------------------
        // Estado
        // --------------------------------------------

        this.state = {

            jobId: null,

            filename: "",

            status: "Aguardando...",

            connected: false,

            processing: false,

            progress: 0,

            currentPage: 0,

            totalPages: 0,

            pageImage: null,

            pdfUrl: null,

            json: {},

            logs: [],

            crops: [],

            statistics: {

                employees: 0,

                activities: 0,

                photos: 0,

                pages: 0,

            },

            startedAt: null,

        };

        // --------------------------------------------
        // Objetos internos
        // --------------------------------------------

        this.ws = null;

        this.polling = null;

        this.timer = null;

        this.destroyed = false;

        // --------------------------------------------
        // DOM
        // --------------------------------------------

        this.cacheDom();

        // --------------------------------------------
        // Inicialização
        // --------------------------------------------

        this.initialize();

    }

    // =====================================================
    // DOM
    // =====================================================

    cacheDom() {

        this.dom = {

            status:

                document.getElementById(
                    "processing-status"
                ),

            documentName:

                document.getElementById(
                    "docName"
                ),

            currentPage:

                document.getElementById(
                    "currentPage"
                ),

            progressBar:

                document.getElementById(
                    "processingBar"
                ),

            pdfViewer:

                document.getElementById(
                    "pdfViewer"
                ),

            pageImage:

                document.getElementById(
                    "pageImage"
                ),

            cropGallery:

                document.getElementById(
                    "cropGallery"
                ),

            jsonResult:

                document.getElementById(
                    "jsonResult"
                ),

            logs:

                document.getElementById(
                    "liveLogs"
                ),

        };

    }

    // =====================================================
    // Inicialização
    // =====================================================

    initialize() {

        this.reset();

        const params = new URLSearchParams(

            window.location.search

        );

        this.state.jobId = params.get(

            "job"

        );

        this.connectWebSocket();

        if (

            this.state.jobId

        ) {

            this.loadJob();

            this.startPolling();

        }

        window.addEventListener(

            "beforeunload",

            () => this.destroy()

        );

    }

    // =====================================================
    // RESET
    // =====================================================

    reset() {

        this.updateStatus(

            "Aguardando..."

        );

        this.updateProgress(

            0

        );

        this.updateCurrentPage(

            0,

            0

        );

        this.updateDocument(

            "-"

        );

        if (

            this.dom.pageImage

        ) {

            this.dom.pageImage.removeAttribute(

                "src"

            );

        }

        if (

            this.dom.pdfViewer

        ) {

            this.dom.pdfViewer.removeAttribute(

                "src"

            );

        }

        if (

            this.dom.cropGallery

        ) {

            this.dom.cropGallery.innerHTML = "";

        }

        if (

            this.dom.logs

        ) {

            this.dom.logs.innerHTML = "";

        }

        if (

            this.dom.jsonResult

        ) {

            this.dom.jsonResult.textContent = "";

        }

        this.state.logs = [];

        this.state.crops = [];

        this.state.json = {};

        this.state.statistics = {

            employees: 0,

            activities: 0,

            photos: 0,

            pages: 0,

        };

    }

    // =====================================================
    // DESTROY
    // =====================================================

    destroy() {

        this.destroyed = true;

        this.stopPolling();

        this.stopTimer();

        if (

            this.ws

        ) {

            try {

                this.ws.close();

            }

            catch (error) {

                console.error(error);

            }

            this.ws = null;

        }

    }
	
	// =====================================================
    // WEBSOCKET
    // =====================================================

    connectWebSocket() {

        const protocol =

            location.protocol === "https:"
                ? "wss"
                : "ws";

        const url =

            `${protocol}://${location.host}/ws`;

        console.info(

            "Conectando WebSocket:",

            url

        );

        this.ws = new WebSocket(url);

        this.ws.onopen = () => {

            console.info(

                "WebSocket conectado."

            );

            this.state.connected = true;

            this.updateStatus(

                this.state.processing
                    ? "Processando..."
                    : "Conectado"

            );

        };

        this.ws.onmessage = (event) => {

            try {

                const data = JSON.parse(

                    event.data

                );

                console.debug(

                    "WS",

                    data

                );

                this.processEvent(

                    data

                );

            }

            catch (error) {

                console.error(

                    error

                );

            }

        };

        this.ws.onerror = (error) => {

            console.error(

                "Erro WebSocket",

                error

            );

        };

        this.ws.onclose = () => {

            console.warn(

                "WebSocket desconectado."

            );

            this.state.connected = false;

            if (

                this.destroyed

            ) {

                return;

            }

            this.updateStatus(

                "Reconectando..."

            );

            setTimeout(

                () => {

                    if (

                        !this.destroyed

                    ) {

                        this.connectWebSocket();

                    }

                },

                2000

            );

        };

    }

    disconnectWebSocket() {

        if (

            this.ws

        ) {

            try {

                this.ws.close();

            }

            catch (error) {

                console.error(

                    error

                );

            }

            this.ws = null;

        }

    }

    // =====================================================
    // EVENTOS
    // =====================================================

    processEvent(event) {

        switch (event.event) {

            case "job_created":

                this.state.jobId =

                    event.job_id;

                this.updateDocument(

                    event.filename

                );

                break;

            case "job_started":

                this.state.processing = true;

                this.state.startedAt =

                    Date.now();

                this.startTimer();

                this.updateStatus(

                    "Iniciando processamento..."

                );

                break;

            case "progress":

                this.updateProgress(

                    event.percent

                );

                this.updateCurrentPage(

                    event.page,

                    event.total

                );

                break;

            case "page_started":

                this.updateStatus(

                    `Página ${event.page}`

                );

                break;

            case "page_finished":

                this.updateStatus(

                    `Página ${event.page} concluída`

                );

                break;

            case "page_image":

                this.updatePageImage(

                    event.image

                );

                break;

            case "crop_found":

                this.addCrop(

                    event.crop

                );

                break;

            case "json":

                this.updateJson(

                    event.json

                );

                break;

            case "statistics":

                this.updateStatistics(

                    event

                );

                break;

            case "employee_found":

                this.receiveEmployee(

                    event.employee

                );

                break;

            case "activity_found":

                this.receiveActivity(

                    event.activity

                );

                break;

            case "photo_found":

                this.receivePhoto(

                    event.photo

                );

                break;

            case "log":

                this.appendLog(

                    event.level,

                    event.message

                );

                break;

            case "job_finished":

                this.state.processing = false;

                this.stopTimer();

                this.updateProgress(

                    100

                );

                this.updateStatus(

                    "Processamento finalizado"

                );

                this.stopPolling();

                break;

            case "job_failed":

                this.state.processing = false;

                this.stopTimer();

                this.updateStatus(

                    "Erro no processamento"

                );

                break;

            default:

                console.debug(

                    "Evento ignorado:",

                    event.event

                );

        }

    }
	
	// =====================================================
    // ATUALIZAÇÃO DA INTERFACE
    // =====================================================

    updateStatus(status) {

        this.state.status = status || "";

        if (this.dom.status) {

            this.dom.status.textContent = this.state.status;

        }

    }

    updateDocument(filename) {

        this.state.filename = filename || "";

        if (this.dom.documentName) {

            this.dom.documentName.textContent =

                this.state.filename || "-";

        }

    }

    updateCurrentPage(page, total) {

        this.state.currentPage = Number(page) || 0;

        this.state.totalPages = Number(total) || 0;

        if (this.dom.currentPage) {

            this.dom.currentPage.textContent =

                `${this.state.currentPage} / ${this.state.totalPages}`;

        }

    }

    updateProgress(percent) {

        percent = Number(percent);

        if (Number.isNaN(percent)) {

            percent = 0;

        }

        percent = Math.max(

            0,

            Math.min(

                100,

                percent

            )

        );

        this.state.progress = percent;

        if (!this.dom.progressBar) {

            return;

        }

        this.dom.progressBar.style.width =

            `${percent}%`;

        this.dom.progressBar.textContent =

            `${Math.round(percent)}%`;

    }

    // =====================================================
    // PDF
    // =====================================================

    updatePdf(url) {

        if (

            !url ||

            !this.dom.pdfViewer

        ) {

            return;

        }

        this.state.pdfUrl = url;

        this.dom.pdfViewer.src = url;

    }

    // =====================================================
    // Página
    // =====================================================

    updatePageImage(image) {

        if (

            !this.dom.pageImage

        ) {

            return;

        }

        if (

            !image

        ) {

            this.dom.pageImage.removeAttribute(

                "src"

            );

            return;

        }

        this.state.pageImage = image;

        this.dom.pageImage.src = image;

    }

    // =====================================================
    // JSON
    // =====================================================

    updateJson(data) {

        this.state.json =

            data || {};

        if (

            !this.dom.jsonResult

        ) {

            return;

        }

        this.dom.jsonResult.textContent =

            JSON.stringify(

                this.state.json,

                null,

                4

            );

    }

    clearJson() {

        this.state.json = {};

        if (

            this.dom.jsonResult

        ) {

            this.dom.jsonResult.textContent = "";

        }

    }

    // =====================================================
    // Estatísticas
    // =====================================================

    updateStatistics(data) {

        if (!data) {

            return;

        }

        this.state.statistics = {

            employees:

                Number(

                    data.employees

                ) || 0,

            activities:

                Number(

                    data.activities

                ) || 0,

            photos:

                Number(

                    data.photos

                ) || 0,

            pages:

                Number(

                    data.pages

                ) || 0,

        };

        console.debug(

            "Estatísticas",

            this.state.statistics

        );

    }

    resetStatistics() {

        this.state.statistics = {

            employees: 0,

            activities: 0,

            photos: 0,

            pages: 0,

        };

    }
	
	// =====================================================
    // CROPS
    // =====================================================

    addCrop(crop) {

        if (!crop) {
            return;
        }

        this.state.crops.push(crop);

        this.renderGallery();

    }

    renderGallery() {

        if (!this.dom.cropGallery) {
            return;
        }

        this.dom.cropGallery.innerHTML = "";

        for (const crop of this.state.crops) {

            const card = document.createElement("div");
            card.className = "crop-card";

            const img = document.createElement("img");
            img.src = crop.image;
            img.alt = crop.name;

            const title = document.createElement("div");
            title.className = "crop-title";
            title.textContent = crop.name;

            card.appendChild(img);
            card.appendChild(title);

            if (crop.bbox) {

                const bbox = document.createElement("small");

                bbox.textContent =
                    `(${crop.bbox.join(", ")})`;

                card.appendChild(bbox);

            }

            card.onclick = () => {

                this.updatePageImage(crop.image);

            };

            this.dom.cropGallery.appendChild(card);

        }

    }

    clearGallery() {

        this.state.crops = [];

        if (this.dom.cropGallery) {

            this.dom.cropGallery.innerHTML = "";

        }

    }

    // =====================================================
    // LOGS
    // =====================================================

    appendLog(level, message) {

        const item = {

            date: new Date(),

            level,

            message,

        };

        this.state.logs.push(item);

        if (!this.dom.logs) {
            return;
        }

        const line = document.createElement("div");

        line.className =

            `log log-${String(level).toLowerCase()}`;

        line.textContent =

            `[${item.date.toLocaleTimeString()}] ${level} - ${message}`;

        this.dom.logs.appendChild(line);

        this.dom.logs.scrollTop =

            this.dom.logs.scrollHeight;

    }

    clearLogs() {

        this.state.logs = [];

        if (this.dom.logs) {

            this.dom.logs.innerHTML = "";

        }

    }

    // =====================================================
    // TIMER
    // =====================================================

    startTimer() {

        this.stopTimer();

        this.state.startedAt = Date.now();

        this.timer = setInterval(() => {

            if (!this.state.startedAt) {
                return;
            }

            const elapsed =

                Math.floor(

                    (Date.now() - this.state.startedAt)

                    / 1000

                );

            console.debug(

                "Tempo:",

                elapsed,

                "segundos"

            );

        }, 1000);

    }

    stopTimer() {

        if (this.timer) {

            clearInterval(this.timer);

            this.timer = null;

        }

    }

    // =====================================================
    // EVENTOS DE EXTRAÇÃO
    // =====================================================

    receiveEmployee(employee) {

        console.info(

            "Colaborador:",

            employee

        );

    }

    receiveActivity(activity) {

        console.info(

            "Atividade:",

            activity

        );

    }

    receivePhoto(photo) {

        console.info(

            "Foto:",

            photo

        );

    }
	
	// =====================================================
    // REST
    // =====================================================

    async loadJob() {

        if (!this.state.jobId) {
            return;
        }

        try {

            const response = await fetch(

                `/api/jobs/${this.state.jobId}`

            );

            if (!response.ok) {
                throw new Error("Job não encontrado.");
            }

            const job = await response.json();

            this.populateJob(job);

        }

        catch (error) {

            console.error(error);

        }

    }

    async refreshJob() {

        await this.loadJob();

    }

    populateJob(job) {

        if (!job) {
            return;
        }

        this.updateDocument(job.filename);

        this.updateStatus(job.status);

        this.updateProgress(job.progress || 0);

        this.updateCurrentPage(

            job.current_page || 0,

            job.total_pages || 0

        );

        if (job.job_id) {

            this.updatePdf(

                `/api/jobs/${job.job_id}/pdf`

            );

        }

    }

    // =====================================================
    // POLLING
    // =====================================================

    startPolling() {

        this.stopPolling();

        this.polling = setInterval(

            () => {

                this.refreshJob();

            },

            5000

        );

    }

    stopPolling() {

        if (this.polling) {

            clearInterval(this.polling);

            this.polling = null;

        }

    }

    // =====================================================
    // LIMPEZA
    // =====================================================

    clear() {

        this.reset();

    }

    // =====================================================
    // DEBUG
    // =====================================================

    debug() {

        console.table(this.state);

    }

    version() {

        return "ProcessingController v5";

    }

}
	
	