<script>
    //Svelte function for dispatching custom events
    import {createEventDispatcher} from 'svelte';
    const dispatch = createEventDispatcher();

    //Variables for the form title text and header message text
    const formTitle = "Upload Form";
    const formHeaderMessage = "Please fill out the form below";

    //Dispatch function which is triggered when the form is submitted, parameter set with function
    //is the form target which is needed to receive the information submitted to the form.
    const formSubmitted = (e)=>{
        dispatch('formSubmitted', e.target);
    }

</script>

<div id="form-holder">
    <!--Form title text set by 'formTitle' variable-->
    <h2>{formTitle}</h2>
    <!--Form header message set by 'formHeaderMessage' variable-->
    <p>{formHeaderMessage}</p>
    <!--Form with on:submit set to 'preventDefault' and to trigger the 'formSubmitted' function. 'preventDefault' is required to
    stop the form from refreshing the page upon submit.-->
    <form on:submit|preventDefault={formSubmitted}>
        <!--Form inputs and buttons use the global styles 'form-input' and 'form-button' respectively-->
        <label for="name-label">Name</label>
        <input name="user-name" type="text" class="form-input" placeholder="Please enter your name...">
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