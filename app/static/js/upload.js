class UploadManager{

    constructor(){

        this.drop=document.getElementById("dropzone");

        this.file=document.getElementById("fileInput");

        this.initialize();

    }

    initialize(){

        if(!this.drop)return;

        this.drop.addEventListener("dragover",(e)=>{

            e.preventDefault();

            this.drop.classList.add("drag");

        });

        this.drop.addEventListener("dragleave",()=>{

            this.drop.classList.remove("drag");

        });

        this.drop.addEventListener("drop",(e)=>{

            e.preventDefault();

            this.drop.classList.remove("drag");

            this.sendFiles(e.dataTransfer.files);

        });

        this.file.addEventListener("change",(e)=>{

            this.sendFiles(e.target.files);

        });

    }

    async sendFiles(files){

        for(const file of files){

            const form=new FormData();

            form.append("file",file);

            const response=await fetch("/api/upload",{

                method:"POST",

                body:form

            });

            const json=await response.json();

            Dashboard.addLog(

                "Upload: "+json.filename

            );

        }

    }

}

window.addEventListener("DOMContentLoaded",()=>{

    new UploadManager();

});