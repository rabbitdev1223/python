<script>
    //Imports for multiple svelte components
    import UploadForm from "./UploadForm.svelte";
    import UploadResult from "./UploadResult.svelte"
    import MissionStatement from "./MissionStatement.svelte";
    import Contact from "./Contact.svelte";

    //Import for util function 'getNextID' which returns a int then increments it
    import {getNextID} from '../../public/scripts/Utils';
    import {csrfToken} from '../store.js';

    //Exposed variable used for determining if user is logged in.
    export let userLoggedIn = false;

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
            //Object to store parsed form data
		    let uploadInfo = {name: ""};

		    /*For loop which runs through all key value pairs sent from the upload request.
		    If the key of the current value is 'user-name' the name value of the 'uploadInfo' variable
		    is set to that keys value, same goes for the 'user-password'*/ 
		    for (const [k, v] of formData.entries()) {
			    if(k == "user-name"){
				    uploadInfo.name = v;
                }
		    }

            /*Makes a fetch request to the upload route of the backend server, and sends over the recieved form data
		    over in JSON format using JSON.stringify. After the response is recieved we check the status of the response
		    through the 'status' value, if the status is 'ok' we add a new successful upload result message, however if the 
            status is 'error' we add a new error upload result message */
		    fetch('api/upload',{
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
                    addUploadResult(getNextID(), "success", "Upload Successful");
                }else if(resJson.status == "error"){
                    addUploadResult(getNextID(), "error", "Upload Failed");
                }
		    })
		    .catch(error => console.log(error));

            e.detail.reset();
        }
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