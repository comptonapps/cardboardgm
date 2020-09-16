class ModalWindow {
    constructor() {
        this.modalWindow = document.createElement('div')
        this.closeButton = document.createElement('button')
        this.init()
    
    }

    init() {
        this.setupModalWindow();
        this.setupCloseButton();
        console.log(this.modalWindow)
    }

    setupModalWindow() {
        this.modalWindow.classList.add('modal-window')
        this.modalWindow.append(this.closeButton)
    }

    setupCloseButton() {
        this.closeButton.classList.add('close-btn')
        this.closeButton.innerText = "CLOSE"
        this.closeButton.addEventListener('click', () => {
            this.modalWindow.remove();
        })
    }
}