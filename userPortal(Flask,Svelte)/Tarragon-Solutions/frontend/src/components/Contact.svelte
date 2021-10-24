<script>
    //Exposed contact variables
    export let contactEmail = "";
    export let contactPhone = "";

</script>

<div id="contact-container">
    <!--Header text for Contact Component-->
    <h2>Contact Us</h2>
    <!--Contact message text-->
    <p class="contact-message">Would you like to get through to us send a <br> message or call</p>
    <!--Contact email & phone set through exposed variables 'contactEmail' & 'contactPhone'-->
    <p>Email: {contactEmail} <br> Phone: {contactPhone}</p>
</div>

<style>
    /*Contact container styling*/
    #contact-container{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 400px;
        background-color: var(--document-secondary-background-color);
    }

    /*Contact header text styling*/
    #contact-container h2{
        color: var(--document-header-text-color);
        font-size: 48pt;
        margin: 8px 0px;
    }

    /*Contact email and phone text styling*/
    #contact-container p{
        text-align: center;
        color: var(--document-header-text-color);
        font-size: 16pt;
    }

    /*Contact message styling*/
    .contact-message{
        text-align: center;
        color: var(--document-header-text-color);
        font-size: 16pt;
        margin-bottom: 22px;
    }

    /*Mobile styling*/
    @media screen and (max-width: 420px){
        #contact-container h2{
            font-size: 36pt;
        }

        #contact-container p{
            font-size: 14pt;
        }

        .contact-message{
            font-size: 14pt;
        }
    }
</style>