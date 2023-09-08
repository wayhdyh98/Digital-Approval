var multirow = []
var allrow = []

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
    var _str = str
    _str = _str.replaceAll("##Page_Break##", `<div class="pagebreak"></div>`)
    _str = _str.replaceAll("##borderless", "--borderless")
    _str = _str.replaceAll("##bordered", "--bordered")
    
    multirow.forEach(item => {
        while (getPosition(_str, `##Table_${item.grouptitle}`, 1) !== _str.length) {
            var start = getPosition(_str, `##Table_${item.grouptitle}`, 1)
            var end = getPosition(_str, `##`, 2) + 2

            var substrdoc = _str.substring(start, end).replaceAll("/\//", "").replaceAll("<p>", "")

            var table = $(`<table id="table-${item.grouptitle}" style="width: 100%;" border>`)
            var thead = $(`<thead id="thead-${item.grouptitle}">`)

            var trHead = $(`<tr id="trHead-${item.grouptitle}">`)

            item.designdocumentquestion.forEach(x => {
                trHead.append(
                    $("<th style='border: 1px solid black; padding: 5px'>").text(x.question)
                )
            })

            trHead.appendTo(thead)

            table.append(thead)

            var tbody = $(`<tbody id="tbody-${item.grouptitle}">`)
            
            if (item.designdocumentquestion.length != 0) {
                var arranswer = item.designdocumentquestion.map((item, idx, arr) => { return item.answer } )
                var idxhighestarranswer = arranswer.reduce((maxI,el,i,arr) => (el.length>arr[maxI].length) ? i : maxI, 0)
                var transposed_arranswer = arranswer[idxhighestarranswer].map((_, colIndex) => arranswer.map(row => row[colIndex]))

                transposed_arranswer.forEach(answer => {
                    var trBody = $(`<tr id="trBody-${item.grouptitle}">`)
                    answer.forEach(x => {
                        trBody.append(
                            $(`<td style="max-width:1px; white-space: normal">`).html(
                                `<span style="word-wrap: break-word; overflow-wrap: break-word">${x}</span>`
                            )
                        )
                    })
                    trBody.appendTo(tbody)
                })
                table.append(tbody)
            }

            _str = replaceBetween(_str, start, end, $('<div></div>').append(table.clone()).html())
        }
    })

    multirow.forEach(item => {
        while (getPosition(_str, `##Card_${item.grouptitle}`, 1) !== _str.length) {
            let start = getPosition(_str, `##Card_${item.grouptitle}`, 1)
            let end = getPosition(_str, `##`, 2) + 2

            const substrdoc = _str.substring(start, end)

            const divParent = $("<div>")

            if (item.designdocumentquestion.length != 0) {
                var arrquestion = item.designdocumentquestion.map((item, idx, arr) => { return item.question } )
                var arranswer = item.designdocumentquestion.map((item, idx, arr) => { return item.answer } )
                var idxhighestarranswer = arranswer.reduce((maxI,el,i,arr) => (el.length>arr[maxI].length) ? i : maxI, 0)
                var transposed_arranswer = arranswer[idxhighestarranswer].map((_, colIndex) => arranswer.map(row => row[colIndex]))
                console.log(transposed_arranswer)
                console.log(arranswer)

                transposed_arranswer.forEach(answer => {
                    const divChild = $('<div style="margin-bottom: 10px; width: fit-content; border: 1px solid black; padding: 4px;">')
                    answer.forEach((x, idx, arr) => {
                        x = x == undefined ? "-" : x
                        divChild.append(
                            `${arrquestion[idx]}: `,
                            `${x}`,
                            $("<br/>")
                        )
                    })
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