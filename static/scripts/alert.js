import ModalWindow from './modalWindow'

class AlertController{
    constructor(title, msg, callback) {
        this.title = title
        this.msg = msg
        this.window = new ModalWindow();
        this.init()
    }

    init() {
        // this.setupElement();
        // this.addTitle();
        // this.addMsg()
        // this.addFormButtons();
        alert("MADE IT")
    }

    setupElement() {
        this.element.id = 'testersChoice';
    }

    addTitle() {
        console.log(this)
        let h1 = this.getNewElement('h1');
        h1.innerText = "Schnikies";
        this.element.append(h1);
    }

    addMsg() {
        let h3 = this.getNewElement('h3');
        h3.innerText = "Tommy Boy";
        this.element.append(h3);
    }

    addFormButtons() {
        let button = this.getNewElement('button')
        button.innerText = "PRESS ME"
        button.addEventListener('click', function() {
            let el = document.querySelector('#testersChoice');
            el.remove();
        })
        this.element.append(button)
    }

    getNewElement = (type) => {
        return document.createElement(type);
    }
}

let alertController = new AlertController("HELL", "YES", function() {
    alert("Callback")
});

