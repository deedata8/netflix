  
function table_to_csv(source, columns) {
    const nrows = source.get_length()
    const lines = [columns.join(',')]

    //alert(JSON.stringify(columns, undefined, 2))

    for (let i = 0; i < nrows; i++) {
        let row = [];
        for (let j = 0; j < columns.length; j++) {
            const column = columns[j]
            let cell = source.data[column][i].toString();
            row.push(cell.includes(',') ? '"' + cell + '"' : cell)
        }
        lines.push(row.join(','))
    }
    return lines.join('\n').concat('\n')
}

const filename = 'data_result.csv'
const filetext = table_to_csv(source, columns)

const blob = new Blob([filetext], { type: 'text/csv;charset=utf-8;' })

//addresses IE
if (navigator.msSaveBlob) {
    navigator.msSaveBlob(blob, filename)
} else {
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = filename
    link.target = '_blank'
    link.style.visibility = 'hidden'
    link.dispatchEvent(new MouseEvent('click'))
}