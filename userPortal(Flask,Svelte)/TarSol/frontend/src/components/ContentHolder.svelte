<script>
    //Imports for multiple svelte components
    import UploadForm from "./UploadForm.svelte";
    import UploadResult from "./UploadResult.svelte"
    import MissionStatement from "./MissionStatement.svelte";
    import Contact from "./Contact.svelte";

    //Imports xlsx to help parse xls and xlsx files, import is bundled into file build
    import XLSX from 'xlsx';

    //Import for util functions and token store
    import {getNextID, isCSVFile, isXLSFile, 
        parseCSVFileToObjectArray, csvHasHeader,
         convertCSVObjectsToObject, setArrayToEmptyStrings} from '../../public/scripts/Utils';
    import {csrfToken} from '../stores/store';

    //Exposed variable used for determining if user is logged in.
    export let userLoggedIn = false;

    //An array of all the currently set header values
    let currentHeaderValues = [];

    //An array of currently active upload result messages, stored in this format {id, status(success/error), message}
    let uploadResultMessages = [];

    //Function for easily adding new upload result messages
    const addUploadResult = (id, status, message)=>{
        uploadResultMessages = [...uploadResultMessages, {id, status, message}]
    }

    //Function which handles what happens when the user tried to upload to the backend
    const uploadFormHandler = (e)=>{
        //Check to make sure user is logged in, could use more security once login backend is established.
        if(userLoggedIn){
             //Takes the information from the upload request and creates a new FormData object which puts the info into an array of key, value pairs
             const formData = new FormData(e.detail);
		    
            //The selected file submitted to the form
            let uploadedFile = null;

            //An object which stores the header values that are submitted to the form
            let headerNames = { licenseNumber: -1, npi: -1, 
                expirationDate: "99/99/9999", zipcode: 123456,};

            
            /*For loop which runs through all key value pairs sent from the upload request.
		    If the key of the current value is 'user-name' the name value of the 'uploadInfo' variable
		    is set to that keys value, same goes for the 'user-password'*/ 
		    for (const [k, v] of formData.entries()) {
			    if(k == "uploaded-file"){
                    if(v != null){
                        uploadedFile = v;
                    }else{
                        addUploadResult(getNextID(), "error", "Upload Failed - No File Selected");
                    }
                }else if(k == "license-number"){
                    headerNames.licenseNumber = v;
                }else if(k == "npi"){
                    headerNames.npi = v;
                }else if(k == "expiration-date"){
                    headerNames.expirationDate = v;
                }else if(k == "zipcode"){
                    headerNames.zipcode = v;
                }
		    }
            
            //Creates a new file reader to read the selected file
            const fileReader = new FileReader();

            //An array which will store the final converted file when parsing is finished
            let convertedFile = [];

            //Function which triggers when the file reader loads a file
            fileReader.onload = (e)=>{

                //Gets the read text from the file reader
                const fileText = e.target.result;

                /*If the file is a .csv it first checks to see if
                the provided csv file has the headers that match the
                ones provided, if not it returns out of the file parsing 
                and adds a new 'UploadResult' error. After that check is done
                it take the read text and passes it through the 'parseCSVFileToObjectArray'
                function which converts the string value passed from the reader
                to an array of objects in the format of {header: 'value', value: 'value'}.
                Once that is finished it then that new array onto the 'convertCSVObjectsToObject'
                function which will generate the final array of objects which has all the desired
                information store in an array of objects in the format of 
                {licenseNumber: 'value', npi: 'value', expDate: 'value', zipcode: 'value'}. This
                final array that is created which is set to the 'convertedFile' variable is the
                information which is sent to the backend server inside the 'data' property
                */
               if(isCSVFile(uploadedFile.name)){
                    if(!csvHasHeader(fileText, headerNames.licenseNumber)||!csvHasHeader(fileText, headerNames.npi)
                    ||!csvHasHeader(fileText, headerNames.expirationDate)||!csvHasHeader(fileText, headerNames.zipcode)){
                        console.log('upload failed');
                        addUploadResult(getNextID(), "error", "Upload Failed - Missing Headers");
                        return;
                    }
                    const csvArray = parseCSVFileToObjectArray(fileText);
                    
                    convertedFile = convertCSVObjectsToObject(csvArray, headerNames);

                }/* When the file is an xls or xlsx file we first start by getting the
                    result from the file reader and creating a new 'Unit8Array' from it,
                    then we take that data and pass it int the 'XLSX.read' function provided
                    by the XLSX node module. Once we have read in the file we create a new
                    constant varibale that will store the first sheet inside the excel file,
                    then we take that sheet and pass it into another function provided by
                    the XLSX module called 'sheet_to_csv' which is used to convert the sheet
                    to csv which is an easier format to work with. Once we have the sheet in
                    csv format we can make sure we have our headers using the same method used
                    for csv files. After the header check is done, we convert the data the same 
                    way we converted the csv files.
                */
                else if(isXLSFile(uploadedFile.name)){
                    let fileData = new Uint8Array(fileReader.result);
                    let parsedData = XLSX.read(fileData, {type: 'array'});

                    const firstSheet = parsedData.Sheets[parsedData.SheetNames[0]];
                    const convertedCSV = XLSX.utils.sheet_to_csv(firstSheet, {blankrows: false});

                    if(!csvHasHeader(convertedCSV, headerNames.licenseNumber)||!csvHasHeader(convertedCSV, headerNames.npi)
                    ||!csvHasHeader(convertedCSV, headerNames.expirationDate)||!csvHasHeader(convertedCSV, headerNames.zipcode)){
                        addUploadResult(getNextID(), "error", "Upload Failed - Missing Headers");
                        return;
                    }
                    
                    const csvObjectsArray = parseCSVFileToObjectArray(convertedCSV);

                    convertedFile = convertCSVObjectsToObject(csvObjectsArray, headerNames);
                }

                /*Once the parsing has been completed we create a new variable called 'uploadInfo'
                which stores the converted file inside the 'data' property, then we call the
                'uploadInformation' function and pass in the uploadInfo along with the name of the file
                for use in 'UploadResult' messages.*/
                let uploadInfo = {data: convertedFile};

                uploadInformation(uploadInfo, uploadedFile.name);
            }

            /*Parse the info from file depending on file type.
             If the file type is csv it is read as text, but if
             it is xls or xlsx it will read it as an array buffer.
             The file type is determined by two util methods 'isCSVFile'
             and 'isXLSFile' which both take the uploaded files name as
             an argument.
            */
            if(isCSVFile(uploadedFile.name)){
                fileReader.readAsText(uploadedFile);
            }else if(isXLSFile(uploadedFile.name)){
                fileReader.readAsArrayBuffer(uploadedFile);
            }
        }
    }

    /*Makes a fetch request to the upload route of the backend server, and sends over the recieved form data
	over in JSON format using JSON.stringify. After the response is recieved we check the status of the response
	through the 'status' value, if the status is 'ok' we add a new successful upload result message and clear
    the current header input values, however if the status is 'error' we add a new error upload result message */
    const uploadInformation = (uploadInfo, fileName)=>{
        fetch('/api/upload',{
		    method: 'POST',
		    mode: 'cors',
		    credentials: 'same-origin',
		    headers:{
				'Content-Type': 'application/json',
				'Access-Control-Allow-Origin': '*',
                "X-CSRFToken": $csrfToken
			},
			body: JSON.stringify(uploadInfo)
		})
		.then(res => res.json())
		.then(resJson => {
            if(resJson.status == "ok"){
                //Adds new successful upload result message that says 'Upload Successful - --FILE-NAME--', then clears the inputs
                
                addUploadResult(getNextID(), "success", `Upload Successful - ${fileName}`);
                currentHeaderValues = setArrayToEmptyStrings(currentHeaderValues);
            }else if(resJson.status == "error"){
                //Adds an error upload result message which says 'Upload Failed - --FILE-NAME--'
                addUploadResult(getNextID(), "error", `Upload Failed - ${fileName}`);
            }
		}).catch(error => {console.log(error);});
    }

</script>

<div id="content-holder">
    <!--UploadForm and Upload Result svelte components (Only visible when the user is logged in)-->
    {#if userLoggedIn}
        <div id="form-container">
            <!--UploadForm has an 'on:formSubmitted' event which is set to the 'uploadFormHandler' function-->
            <UploadForm on:formSubmitted={uploadFormHandler} ></UploadForm>
            <!--UploadResult has an exposed array called 'uploadResults' which is bound to the local 'uploadResultMessages' array-->
            <UploadResult bind:uploadResults={uploadResultMessages} ></UploadResult>
        </div>
    {/if}

    <!--MissionStatement svelte component-->
    <MissionStatement></MissionStatement>
    <!--Contact svelte component, has exposed variables for 'contactEmail' and 'contactPhone'-->
    <Contact contactEmail="support@tarragon.solutions" contactPhone="+123456789"></Contact>
    
    <!--Content slot for easily adding additional content to the ContentHolder-->
    <slot name="content-slot-one"></slot>
    <slot name="content-slot-two"></slot>
    <slot name="content-slot-three"></slot>
</div>

<style>
    /*UploadForm and UploadResult container styling*/
    #form-container{
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-around;
        flex-wrap: wrap;
        width: 100%;
        height: auto;
        margin-top: 8px;
    }
</style>
