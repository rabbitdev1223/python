let currentID = 0;
export const getNextID = () => {
    return currentID++;
}

export const setArrayToEmptyStrings = (array) =>{
    for(let i = 0; i < array.length; i++){
        array[i] = "";
    }
    return array;
}


export const convertCSVObjectsToObject = (csvObjects, headerNames)=>{
    let licenseNums = [];
    let NPIs = [];
    let expDates = [];
    let zips = [];

    csvObjects.array.forEach(e=>{
        if(e.header == headerNames.licenseNumber){
            licenseNums = [...licenseNums, e.value]
        }else if(e.header == headerNames.npi){
            NPIs = [...NPIs, e.value]
        }else if(e.header == headerNames.expirationDate){
            expDates = [...expDates, e.value]
        }else if(e.header == headerNames.zipcode){
            zips = [...zips, e.value]
        }
    });

    let completedList = [];

    for(let i = 0; i < csvObjects.rowCount; i++){
        completedList = [...completedList, 
        {licenseNumber: licenseNums[i], npi: NPIs[i], expDate: expDates[i], zipcode: zips[i]}];
    }

    return completedList;
}

const csvDelimiter = ",";
export const getFileExtension = (filename)=>{
    let nameParts = filename.split('.');
    return nameParts[nameParts.length - 1];
}

export const isCSVFile = (filename)=>{
    let extension = getFileExtension(filename);
    if(extension.toLowerCase() == 'csv'){
        return true;
    }

    return false;
}

export const isXLSFile = (filename)=>{
    let extension = getFileExtension(filename).toLowerCase();
    if(extension == 'xls' || extension == 'xlsx'){
        return true;
    }

    return false;
}

export const csvHasHeader = (csvString, headerName) => {
    const csvHeader = csvString.slice(0, csvString.indexOf("\n")).split(csvDelimiter);
    console.log(csvHeader,headerName);
    if(csvHeader.includes(headerName) || csvHeader.includes(headerName+"\r")){
        return true;
    }

    return false;
}

//Parses CSV file into an array
export const parseCSVFileToArray = (csvString)=>{
    const csvHeader = csvString.slice(0, csvString.indexOf("\n")).split(csvDelimiter);
    const csvRows = csvString.slice(csvString.indexOf("\n") + 1).split("\n");

    const csvArray = csvRows.map((row)=>{
        const csvValues = row.split(csvDelimiter);
        const reducedHeaders = csvHeader.reduce((object, header, index)=>{
            object[header] = csvValues[index];
            return object;
        }, {});
        return reducedHeaders;
    });

    return csvArray;
}

export const parseCSVFileToObjectArray = (csvString) => {
    const csvHeaders = csvString.slice(0, csvString.indexOf("\n")).split(csvDelimiter);
    const csvRows = csvString.slice(csvString.indexOf("\n") + 1).split("\n");

    let csvArray = [];

    let mappedRows = [];

    csvRows.forEach((row)=>{
        mappedRows = [...mappedRows, row.split(csvDelimiter)];
    });

    for (let h = 0; h < csvHeaders.length; h++) {
        for (let r = 0; r < csvRows.length; r++) {
            if((csvHeaders[h] != null && csvHeaders[h] !== "") && (mappedRows[r][h] != null && mappedRows[r][h] !== "")){
                if(csvHeaders[h].indexOf('\r') !== -1){
                    csvHeaders[h] = csvHeaders[h].substring(0, csvHeaders[h].indexOf('\r'));
                }
                
                if(mappedRows[r][h].indexOf('\r') !== -1){
                    mappedRows[r][h] = mappedRows[r][h].substring(0, mappedRows[r][h].indexOf('\r'));
                }
    
                csvArray = [...csvArray, {header: csvHeaders[h], value: mappedRows[r][h]}]
            }else{
                continue;
            }
        }
    }

    return {
        array: csvArray,
        headerCount: csvHeaders.length,
        rowCount: csvRows.length
    };
}