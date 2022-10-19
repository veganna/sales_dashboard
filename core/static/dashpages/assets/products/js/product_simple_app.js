class ProductSimpleApp {
    constructor(){
        this.formBasic = document.querySelector('#productBasicForm')
        this.formGallery = document.querySelector('#productGalleryForm')
        this.formShipping = document.querySelector('#productShippingForm')
        this.formVisibility = document.querySelector('#productVisibilityForm')
        this.formMetadata = document.querySelector('#productMetadataForm')
        this._preventFormSubmit()
    }
    
    _preventFormSubmit(){
        this.formBasic.addEventListener('submit', e => e.preventDefault())
        this.formGallery.addEventListener('submit', e => e.preventDefault())
        this.formShipping.addEventListener('submit', e => e.preventDefault())
        this.formVisibility.addEventListener('submit', e => e.preventDefault())
        this.formMetadata.addEventListener('submit', e => e.preventDefault())
    }

    _buildFormData(form){
        const formData = new FormData(form)
        const data = {}
        for (let [key, value] of formData.entries()) {
            if (key == 'csrfmiddlewaretoken'){
                continue
            }
            //if multiple values
            if (data.hasOwnProperty(key)){
                data[key].push(value)
            }else{
                data[key] = [value]
            }
        }
        return data
    }

    _validate(){
        return true
    }

    _submit(){
        let validated_data = {}
        if (this._validate()){
            validated_data['basic'] = this._buildFormData(this.formBasic)
            validated_data['gallery'] = this._buildFormData(this.formGallery)
            validated_data['shipping'] = this._buildFormData(this.formShipping)
            validated_data['visibility'] = this._buildFormData(this.formVisibility)
            validated_data['metadata'] = this._buildFormData(this.formMetadata)
        }

        const url = window.location.href?.split('#')[0]
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'multipart/form-data boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',
                'X-CSRFToken': csrfToken,
                
            },
            body: this._build_data(validated_data)
        }

        fetch(url, options).then(
            response => response.json()
        ).then(
            data => {
                console.log(data)
            }
        ).catch(
            error => console.log(error)
        )
    }   
    
    _build_data(validated_data){
        let data = new FormData()
        //build basic data
        let basic = validated_data['basic']
        for (let key in basic){
            data.append(key, basic[key])
        }
        //build gallery data
        let _gallery = validated_data['gallery']
        let _gallery_list = this._buildGallery(_gallery)
        for (let i = 0; i < _gallery_list.length; i++){
            data.append('gallery', _gallery_list[i])
        }
        //build shipping data
        let shipping = validated_data['shipping']
        for (let key in shipping){
            data.append(key, shipping[key])
        }
        //build visibility data
        let visibility = validated_data['visibility']
        for (let key in visibility){
            data.append(key, visibility[key])
        }
        //build metadata data
        let metadata = validated_data['metadata']
        for (let key in metadata){
            data.append(key, metadata[key])
        }
        return data
    }

    _buildGallery(gallery){
        var gallery = gallery['file']
        var gallery_list = []
        for (let i = 0; i < gallery.length; i++){
            gallery_list.push(gallery[i])
        }
        return gallery_list
    }
}

var productSimpleApp = new ProductSimpleApp()