class RDOWebSocket{

    constructor(){

        this.connect();

    }

    connect(){

        const protocol=

            location.protocol==="https:"?

            "wss":"ws";

        this.ws=new WebSocket(

            protocol+

            "://"+

            location.host+

            "/ws"

        );

        this.ws.onopen=()=>{

            Dashboard.addLog(

                "WebSocket conectado."

            );

        };

        this.ws.onclose=()=>{

            Dashboard.addLog(

                "Reconectando..."

            );

            setTimeout(()=>{

                this.connect();

            },3000);

        };

        this.ws.onmessage=(msg)=>{

            const data=JSON.parse(msg.data);

            this.process(data);

        };

    }

    process(event){

        switch(event.type){

            case "log":

                Dashboard.addLog(

                    event.message

                );

                break;

            case "job":

                app.loadJobs();

                break;

            case "progress":

                Dashboard.addLog(

                    "Página "+

                    event.page+

                    " - "+

                    event.step

                );

                app.loadJobs();

                break;

            case "finished":

                Dashboard.addLog(

                    "Job finalizado."

                );

                app.loadJobs();

                break;

        }

    }

}