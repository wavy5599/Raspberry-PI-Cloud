const $ = (sel)=>document.querySelector(sel);
    const fileInput = $("#fileInput");
    const uploadBtn = $("#uploadBtn");
    const fileList  = $("#fileList");

    // fetch list on load
    window.addEventListener("DOMContentLoaded", refreshList);

    uploadBtn.addEventListener("click", async ()=>{
      const file = fileInput.files[0];
      if(!file){alert("Choose a file first");return;}
      const fd = new FormData(); fd.append("file", file);
      try{
        await fetch("/upload",{method:"POST",body:fd});
        fileInput.value="";
        refreshList();
      }catch(e){console.error(e);alert("Upload failed");}
    });

    async function refreshList(){
      fileList.innerHTML = '<li style="opacity:.6">Loading…</li>';
      try{
        const res = await fetch("/files");
        const files = await res.json();
        if(!files.length){fileList.innerHTML='<li style="opacity:.6">No files yet</li>';return;}
        fileList.innerHTML = files.map(name=>`<li>
            <a href="/files/${encodeURIComponent(name)}" target="_blank">${name}</a>
            <button class="delete" onclick="del('${encodeURIComponent(name)}')">✕</button>
          </li>`).join("");
      }catch(e){fileList.innerHTML='<li>Error loading list</li>';console.error(e);}  
    }

    async function del(name){
      if(!confirm("Delete " + decodeURIComponent(name) + "?")) return;
      try{
        const res = await fetch(`/files/${name}`,{method:"DELETE"});
        if(res.ok) refreshList(); else throw new Error();
      }catch(e){alert("Delete failed");console.error(e);}  
    }