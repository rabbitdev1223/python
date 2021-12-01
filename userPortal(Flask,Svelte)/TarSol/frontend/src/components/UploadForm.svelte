<script>
    //Svelte function for dispatching custom events
    import {createEventDispatcher} from 'svelte';
    import { excel2json } from 'js2excel';
    import {csrfToken} from '../stores/store';

    const dispatch = createEventDispatcher();

    //Import for the utility function to clear the specified array to blank strings
    import {setArrayToEmptyStrings} from '../../public/scripts/Utils';

    //Variables for the form title text and header message text
    const formTitle = "Upload Form";
    const formHeaderMessage = "Please fill out the form below";

    //license num,npi,exp date,zipcode
    export let headerInputValues = ["","","",""];

    //Selected files
    let files;

    //Selected file text
    let fileNameText = "No file selected..."

    //Dispatch function which is triggered when the form is submitted, parameter set with function
    //is the form target which is needed to receive the information submitted to the form.

    const get_what_we_need = function(headvals,data){
        // Takes in headervals key:val pairs. Key is our internal
        // label and value is the label found on the document.
        // This will get only those 4 columns from the document
        //  (data) and return as a list of objects
        console.log('===============');
        console.log(data);
        console.log(headvals);
        let outdata = []
        return new Promise((resolve,reject)=>{
            try{
                for(let i = 0;i<data.length;i++){
                    outdata.push({
                        'npi':data[i][headvals['npi']],
                        'lic':data[i][headvals['lic']],
                        'exp':data[i][headvals['exp']],
                        'zip':data[i][headvals['zip']]
                    })
                }
                
                resolve(outdata);
            }
            catch(err){
                reject(err);
            }

        })
    };


    const formSubmitted = (e)=>{
        e.preventDefault();
        if(files == undefined || files.length == 0 ) {
            showErrorMessage = true;
            console.log("Please select file first.")
            return 0;
        } 
        try {
                let headvals = {
                    'lic':headerInputValues[0],
                    'npi':headerInputValues[1],
                    'exp':headerInputValues[2],
                    'zip':headerInputValues[3]
                }
                excel2json(files, (data) => {
                    get_what_we_need(headvals,data['Sheet1'])
                    .then((outdata)=>{
                        //console.log(outdata);
                        fetch('/api/jsonfromexcel',{
                        method: 'POST',
                        mode: 'cors',
                        credentials: 'same-origin',
                        headers:{
                            'Content-Type': 'application/json',
                            'Access-Control-Allow-Origin': '*',
                            "X-CSRFToken": $csrfToken
                        },
                        body: JSON.stringify({data:outdata, handlevalues: headvals})
                    })
                    .then(res => res.json())
                    .then(resJson => {
                        console.log(resJson);
                    })
                    .catch(error => {
                        console.error(error);
                        // currentErrorMessage = "Error Connection!";
                        // showErrorMessage = true;
                    });

                    })


                }, 'excel2json')
        } catch (e) {
            console.error('export error');
        }
        dispatch('formSubmitted', e.target);
    }

    //Updates the file text when the selected file changes
    const updateSelectedFile = ()=>{
        //Verifies that a file was selected from the dialog, if not sets 'fileNameText' equal to "No file selected"
        if(files != null){
            if(files.length > 0){
                //Sets 'fileNameText' equal to the name of the selected file
                fileNameText = files[0].name;
                //Uses 'setArrayToEmptyStrings' ti clear array then sets the header inputs to the cleared list
                headerInputValues = setArrayToEmptyStrings(headerInputValues);
                return;
            }
        }

        fileNameText = "No file selected...";
    }

</script>

<div id="form-holder">
    <!--Form title text set by 'formTitle' variable-->
    <h2>{formTitle}</h2>
    <!--Form header message set by 'formHeaderMessage' variable-->
    <p>{formHeaderMessage}</p>
    <!--Form with on:submit set to 'preventDefault' and to trigger the 'formSubmitted' function. 'preventDefault' is required to
    stop the form from refreshing the page upon submit.-->
    <form id="" on:submit|preventDefault={formSubmitted}>
        <!--Form inputs and buttons use the global styles 'form-input' and 'form-button' respectively-->

        <!--Label for the file select input, used for styling-->
        <label for="uploaded-file"  class="form-file-input" >
            <p>Select an XLSX, XLS, or CSV file || {fileNameText}</p>
        </label>
        <!--File select input which only accepts .xlsx, .xls, and .csv. Also runs 'updateSelectedFile' when the file selected is changed-->
        <input bind:files id="uploaded-file" name="uploaded-file" type="file" accept=".xlsx,.xls,.csv" on:change={updateSelectedFile}>
        
        <!--License header label and input-->
        <label for="license-number-input">License Number</label>
        <input type="text" id="license-number-input" name="license-number" class="form-input" bind:value={headerInputValues[0]} required placeholder="Enter the column name which contains license numbers">
        
        <!--NPI header label and input-->
        <label for="npi-input">NPI</label>
        <input type="text" id="npi-input" name="npi" class="form-input" bind:value={headerInputValues[1]} required placeholder="Enter the column name which contains NPIs">
       
        <!--Expiration Date header label and input-->
        <label for="expiration-date-input">Expiration Date</label>
        <input type="text" id="expiration-date-input" name="expiration-date" class="form-input" bind:value={headerInputValues[2]} required placeholder="Enter the column name which contains license expiration dates">
        
        <!--Zipcode header label and input-->
        <label for="zipcode-input">Zipcode</label>
        <input type="text" id="zipcode-input" name="zipcode" class="form-input" bind:value={headerInputValues[3]} required placeholder="Enter the column name which contains zipcodes">

        <!--Form submit button-->
        <button type="submit" class="form-button">Upload</button>
    </form>
</div>

<style>
    /*UploadForm container styling*/
    #form-holder{
        min-width: 200px;
        width: 600px;
        max-width: auto;
        min-height: 200px;
        height: 600px;
        max-height: auto;
        background-color: var(--document-form-background-color);
        border: 1px solid var(--document-form-border-color);
        border-radius: var(--document-form-border-radius);
        padding: 12px;
        margin: 4px;
    }

    /*UploadForm form styling*/
    #form-holder form{
        display: flex;
        flex-direction: column;
        margin-top: 10px;
        margin-bottom: 6px;
    }

    /*UploadForm form labels styling*/
    #form-holder form label{
        font-weight: bold;
        color: var(--document-text-primary-color);
        margin-top: 18px;
    }

    /*UploadForm header text styling*/
    #form-holder h2{
        color: var(--document-form-header-title-color);
        padding-bottom: 4px;
    }

    /*UploadForm header message text styling*/
    #form-holder p{
        color: var(--document-form-header-message-color);
    }
</style>
