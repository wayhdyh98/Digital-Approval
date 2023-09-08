var multirow = []

$(document).ready(function () {
    console.log("Ready.");
});

function getPosition(string, subString, index) {
    return string.split(subString, index).join(subString).length
}

function replaceBetween(origin, startIndex, endIndex, insertion) {
    return origin.substring(0, startIndex) + insertion + origin.substring(endIndex)
}

function getQuestionAnswer(string, subString, cond) {
    var arr = string.split(subString)
    if (cond <= 0) {
        return arr.slice(0, arr.length - 1).map(val => val.match(/"([^"]+)"/)[1])
    } else {
        return arr.slice(0, arr.length - 1).map(val => val.match(/@([^@]+)/)[1])
    }
}

function replaceTable(str) {
    var _str = str.replaceAll(/##Answer(.*?)##/g, `?`)
    _str = _str.replaceAll("##Page_Break##", `<div class="pagebreak"> <em>-- Page Break --</em></div>`)
    _str = _str.replaceAll(/##Authorisasi(.*?)##/g, `<img src="https://apps.mpm-motor.com/it/mpmqrcode/Home?d=preview_authorization" width="120px" height="120px">`)
    _str = _str.replaceAll("##borderless", "--borderless")
    _str = _str.replaceAll("##bordered", "--bordered")

    var auth_str = _str.match(/##Nama_Authorisasi_(.*?)##/g)
    if (auth_str) {
        auth_str.forEach(item => {
            var i = item.replace(/[^0-9.]/g, '')
            _str = _str.replaceAll(`##Nama_Authorisasi_${i}##`, `NamaAuth_${i}`)
        })
    }

    var title_str = _str.match(/##Title_Authorisasi_(.*?)##/g)
    if (title_str) {
        title_str.forEach(item => {
            var i = item.replace(/[^0-9.]/g, '')
            _str = _str.replaceAll(`##Title_Authorisasi_${i}##`, `TitleAuth_${i}`)
        })
    }
    
    multirow.forEach(item => {
        while (getPosition(_str, `##Table_${item.grouptitle}`, 1) !== _str.length) {
            var start = getPosition(_str, `##Table_${item.grouptitle}`, 1)
            var end = getPosition(_str, `##`, 2) + 2

            var substrdoc = _str.substring(start, end).replaceAll("/\//", "").replaceAll("<p>", "")

            console.log(substrdoc)

            var designdocumentquestion = getQuestionAnswer(substrdoc, ';', 0)
            var designdocumentquestionanswers = getQuestionAnswer(substrdoc, ';', 1)

            var table = $(`<table id="table-${item.grouptitle}" border>`)
            var thead = $(`<thead id="thead-${item.grouptitle}">`)

            var trHead = $(`<tr id="trHead-${item.grouptitle}">`)
            designdocumentquestion.forEach(question => {
                trHead.append(
                    $("<th style='border: 1px solid black; padding: 5px'>").text(question)
                )
            })

            trHead.appendTo(thead)

            table.append(thead)

            if (item.designdocumentquestion.length != 0) {
                const tbody = $(`<tbody id="tbody-${item.grouptitle}">`)
                const trBody = $(`<tr id="trBody-${item.grouptitle}">`)
                item.designdocumentquestion.forEach(x => {
                    trBody.append(
                        $("<td style='border: 1px solid black; padding: 5px'>").text("dummy_column")
                    )
                    trBody.appendTo(tbody)
                    table.append(tbody)
                })
            }

            _str = replaceBetween(_str, start, end, $('<div></div>').append(table.clone()).html())
        }
    })

    multirow.forEach(item => {
        while (getPosition(_str, `##Card_${item.grouptitle}`, 1) !== _str.length) {
            let start = getPosition(_str, `##Card_${item.grouptitle}`, 1)
            let end = getPosition(_str, `##`, 2) + 2

            const substrdoc = _str.substring(start, end)

            const designdocumentquestion = getQuestionAnswer(substrdoc, ';', 0)
            const designdocumentquestionanswers = getQuestionAnswer(substrdoc, ';', 1)

            const divParent = $("<div>")

            if (item.designdocumentquestion.length != 0) {
                const divChild = $('<div style="margin-bottom: 10px; width: fit-content; border: 1px solid black; padding: 4px;">')
                item.designdocumentquestion.forEach(x => {
                    divChild.append(
                        `${x.question}: `,
                        `dummy_answer`,
                        $("<br/>")
                    )
                    divParent.append(divChild)
                })
            }

            _str = replaceBetween(_str, start, end, $('<div></div>').append(divParent.clone()).html())
        }
    })

    return _str
}

function reArrangePosition(string) {
    for (var [idx, item] of multirow.entries()) {
        findres = string.indexOf(item.grouptitle)
        if (findres != -1) {
            multirow[idx]["position"] = findres
        }
    }
    multirow.sort((a, b) => { return a.position - b.position })
}