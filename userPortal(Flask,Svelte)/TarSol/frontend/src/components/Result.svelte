<script>
    //Svelte function for dispatching custom events
    import {createEventDispatcher} from 'svelte';
    const dispatch = createEventDispatcher();

    //Exposed resultID variable which is set by the Upload Result svelte component
    export let resultID = 0;

    //Exposed resultMessage variable which is set by the Upload Result svelte component
    export let resultMessage = "Example Result";

    //Possible result types 'success' or 'error', determines whether it shows a green checkmark icon or a red cross
    export let resultType = "success";

    //Paths to status icon of the upload result.
    let statusImageSrc = ["assets/result_success.png", "assets/result_error.png"];

    //Dispatch function for clearing the specified result from the UploadResult component.
    const clearResult = (e)=>{
        dispatch("clearResult", e);
    }
</script>

<div id="result-container">
    <!--Container for the result status icon, shows green checkmark if 'resultType' is equal to "success" 
        and a red cross if it is equal "error"-->
    <div id="status-icon">
        {#if resultType == "success"}
            <img src={statusImageSrc[0]} alt="result-success">
        {:else if resultType == "error"}
            <img src={statusImageSrc[1]} alt="result-error">
        {/if}
    </div>
    <!--The result message set by the exposed 'resultMessage' variable-->
    <p>{resultMessage}</p>

    <!--Button to remove the result from the UploadRequest component, triggers clearResult function when button is clicked-->
    <button on:click={()=>{clearResult(resultID)}}>Clear</button>
</div>

<style>
    /*Result container styling*/
    #result-container{
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        width: auto;
        height: auto;
        background-color: var(--form-input-focused-background-color);
        color: var(--form-input-text-color);
        border: 1px solid var(--form-input-border-color);
        border-radius: var(--form-input-border-radius);
        padding: 6px;
        margin: 8px 0px;
    }
    
    /*Result status icon styling*/
    #result-container img{
        width: 24px;
        height: 24px;
    }

    /*Result clear button styling*/
    #result-container button{
        padding: 4px 12px;
        border: none;
        border-radius: var(--form-button-border-radius);
        color: var(--form-button-text-color);
        background-color: var(--form-button-normal-background-color);
        transition: background-color 0.4s;
    }

    /*Result clear button hover styling*/
    #result-container button:hover{
        background-color: var(--form-button-hover-background-color);
    }
</style>