<script>
    //Imports the Result svelte component
    import Result from './Result.svelte';

    //An array of all active upload result objects
    export let uploadResults = [];
    
    //Function to remove result by ID
    const removeResult = (id)=>{
        uploadResults = uploadResults.filter(res => res.id != id)
    }

    //Timer which runs every 2 seconds and makes sure the UploadResult component is always scrolled all the way to the bottom.
    window.setInterval(()=>{
        var results = document.getElementById('result-container');
        if(results != null){
            results.scrollTop = results.scrollHeight;
        }
    }, 2000)
</script>

<div id="upload-result-container">
    <!--Header text for the Upload Result svelte component-->
    <h2>Upload Result</h2>
    <!--Container for all active Result svelte components-->
    <div id="result-container">
        {#each uploadResults as result}
            <!--Creates a Result svelte component for each active result from exposed 'uploadResults' array and sets specified values
            of the current result.-->
            <Result resultID={result.id} resultType={result.status} resultMessage={result.message} on:clearResult={removeResult(result.id)}></Result>
        {/each}
    </div>
</div>

<style>
    /*UploadResult container styling*/
    #upload-result-container{
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
        overflow-y: hidden;
    }

    /*UploadResult result container styling*/
    #result-container{
        width: 100%;
        height: 560px;
        max-height: 560px;
        overflow-y: scroll;
        scrollbar-width: 1px;
    }

    /*Scrollbar styling*/
    #result-container::-webkit-scrollbar{
        width: 1px;
    }

    /*UploadResult header text styling*/
    #upload-result-container h2{
        color: var(--document-form-header-title-color);
        padding-bottom: 4px;
    }
</style>