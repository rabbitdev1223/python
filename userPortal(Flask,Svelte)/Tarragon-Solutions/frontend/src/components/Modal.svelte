<script>
    //Exposed variable the specifies the modal's title text
    export let modalTitleText = "Example Modal";
</script>

<!--Container for the modal which passes its on:click function to the parent element-->
<div id="modal-container" on:click>
    <!--Modal title text set by exposed variable 'modalTitleText'-->
    <h1>{modalTitleText}</h1>
    <!--Modal slot to easily add different content to modal component-->
    <slot name="modal-slot" ></slot>
</div>

<style>
    /*Modal container styling*/
    #modal-container{
        position: fixed;
        display: flex;
        top: 0px;
        left: 0px;
        width: 100%;
        height: 100%;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background-color: var(--modal-background-color);
        color: var(--modal-text-color);
    }
</style>