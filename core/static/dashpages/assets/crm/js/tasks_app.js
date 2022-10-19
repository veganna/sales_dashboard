class Tasks{
    
    constructor(context){
        this.context = context;
        this._build();
    }

    _build(index=null){
        if ( index == null){
            let contextItem = this.context[0];
            
            let html = `
                <div class="offcanvas-header side-fix" style="border-bottom: 1px solid #e3e3e3 !important; padding-bottom: 0 !important; align-content: flex-start; align-items: flex-start;" >
                    <div class="">
                        <h5 id="offcanvasRightLabel">${contextItem.task}</h5>
                    </div>
                    <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
                </div>
                <div class="offcanvas-body side-bar-fix"> 
                    <div>
                        <div class="row">
                            <div class="col-6">
                                <h4 class="mb-0">${contextItem.name}</h4>
                                <p class="name-text mb-0">Harvesting Circles LLC</p>
                                <a href="tel: ${contextItem.phone}" target="_blank" class="mb-0">${contextItem.phone}</a>
                                <div class="tiny-logos mt-0">
                                    <a href="mailto: ${contextItem.name}" target="_blank" class="tiny-icons"><i class=" ri-mail-fill" ></i></a>
                                    <a href="${contextItem.linkedin}" target="_blank" class="tiny-icons"><i class="ri-linkedin-box-fill" ></i></a>
                                    <a href="${contextItem.website}" target="_blank" class="tiny-icons"><i class="ri-external-link-fill"></i> </a>
                                </div>
                            </div>
                        </div>
                        <h5>Notes:</h5>
                        <form id="add-note" data-id="${contextItem.id}" method="post">
                            <textarea id="elm1" name="area"></textarea>
                        </form>
                    </div>

                    <div class="row">
                        <div class="col">
                            <div class="bottom-actions">

                                <button type="button" onclick="tasks.delete(${contextItem.index})" class="btn btn-danger waves-effect waves-light " >Delete  <i class=" ri-delete-bin-line"></i></button>
                                <button type="button" onclick="tasks.complete(${contextItem.index})" class="btn btn-info quick-actions-item waves-effect waves-light">Complete <i class="ri-check-line"></i></button>
                                    
                            </div>
                        </div>
                    </div>
                
                </div>
            `;
            let container = document.querySelector('#offcanvasRight')
            container.innerHTML = html;
            return;
        }else{
                let contextItem = this.context?.find(x => x.index == index);
                let html = `
                <div class="offcanvas-header side-fix" style="border-bottom: 1px solid #e3e3e3 !important; padding-bottom: 0 !important; align-content: flex-start; align-items: flex-start;" >
                    <div class="">
                        <h5 id="offcanvasRightLabel">${contextItem.task}</h5>
                    </div>
                    <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
                </div>
                <div class="offcanvas-body side-bar-fix"> 
                    <div>
                        <div class="row">
                            <div class="col-6">
                                <h4 class="mb-0">${contextItem.name}</h4>
                                <p class="name-text mb-0">Harvesting Circles LLC</p>
                                <a href="tel: ${contextItem.phone}" target="_blank" class="mb-0">${contextItem.phone}</a>
                                <div class="tiny-logos mt-0">
                                    <a href="mailto: ${contextItem.name}" target="_blank" class="tiny-icons"><i class=" ri-mail-fill" ></i></a>
                                    <a href="${contextItem.linkedin}" target="_blank" class="tiny-icons"><i class="ri-linkedin-box-fill" ></i></a>
                                    <a href="${contextItem.website}" target="_blank" class="tiny-icons"><i class="ri-external-link-fill"></i> </a>
                                </div>
                            </div>
                        </div>
                        <h5>Notes:</h5>
                        <form id="${contextItem.id}" onsubmit="(e) => e.preventDefault()" method="post">
                            <textarea onchange="tasks.add_note(${contextItem.id})" id="elm1" name="area"></textarea>
                        </form>
                    </div>

                    <div class="row">
                        <div class="col">
                            <div class="bottom-actions">
                                <button type="button" onclick="tasks.complete(${contextItem.index})" class="btn btn-info quick-actions-item waves-effect waves-light">Complete <i class="ri-check-line"></i></button>
                            </div>
                        </div>
                    </div>
                
                </div>
            `;
            let container = document.querySelector('#offcanvasRight')
            container.style.visibility = "hidden";
            container.classList.remove('show');
            this._chill()
            container.innerHTML = html;
            container.style.visibility = "visible";
            container.classList.add('show');

            return;
            }
        }

        _chill(){
            return new Promise((resolve, reject) => {
                setTimeout(() => {
                    resolve();
                }, 500)
            })
        }

        complete(index){
            let contextItem = this.context[index-1];
            let url = window.location.href?.split('#')[0];
            let csrf_token = document.querySelector('[name="csrfmiddlewaretoken"]').value;
            let data = {
                'id': contextItem.id,
                'action': 'complete'
            }
            fetch(url,{
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrf_token,
                },
                body: JSON.stringify(data)
            }).catch(
                error => alert(error)
            )
            let next = index + 1;
            this._continue(next);
            return;
        }

        add_note(index){
            let contextItem = this.context[index-1];
            let url = window.location.href?.split('#')[0];
            let csrf_token = document.querySelector('[name="csrfmiddlewaretoken"]').value;
            let data = {
                'id': contextItem.id,
                'action': 'add_note',
                'note': document.querySelector('#elm1').value
            }
            fetch(url,{
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrf_token,
                },
                body: JSON.stringify(data)
            }).catch(
                error => alert(error)
            )
            return;
        }

        _continue(index){
            if (this.context.find(x => x.index == index)){
                this._build(index);
            }else{
                window.location.reload();
            }
        }

        mass_complete(){
            let inputs = document.querySelectorAll('input[type="checkbox"]');
            if (inputs.length == 0) return alert('No tasks to complete');
            let ids = [];
            let url = window.location.href?.split('#')[0];
            let csrf_token = document.querySelector('[name="csrfmiddlewaretoken"]').value;
            inputs.forEach(input => {
                if (input.checked){
                    if (!isNaN(input.id)){
                        ids.push(input.id);
                    }                 
                }
            })
            let data = {
                'ids': ids,
                'action': 'mass_complete'
            }
            fetch(url,{
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrf_token,
                },
                body: JSON.stringify(data)
            }).catch(
                error => alert(error)
            )
            window.location.reload();
            return;
        }

        mass_select(id){
            let main_input = document.querySelector(`#${id}`);
            if (main_input.checked){
                let inputs = document.querySelectorAll('input[type="checkbox"]');
                inputs.forEach(input => {
                    input.checked = true;
                })
            }else{
                let inputs = document.querySelectorAll('input[type="checkbox"]');
                inputs.forEach(input => {
                    input.checked = false;
                })
            }
            
        }
}
