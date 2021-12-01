<script></script>

<div id="banner-container">
    <!--Header Text for the Welcome Banner-->
    <h2>Welcome to Tarragon Solutions</h2>
    <!--Welcome banner message text-->
    <p>We are cost effective, user friendly <br>
    and industrial advancing set of services</p>
</div>

<style>
    /*Banner Container Styling*/
    #banner-container{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 400px;
        text-align: center;
    }

    /*Banner header text styling*/
    #banner-container h2{
        color: var(--document-text-header-color);
        font-size: 48pt;
        margin: 8px 0px;
    }

    /*Banner message styling*/
    #banner-container p{
        text-align: center;
        color: var(--document-text-primary-color);
        font-size: 18pt;
    }


    /*Mobile banner styling*/
    @media screen and (max-width: 630px){
        #banner-container h2{
            font-size: 40pt;
        }

        #banner-container p{
            font-size: 12pt;
        }
    }

    @media screen and (max-width: 420px){
        #banner-container h2{
            font-size: 36pt;
        }

        #banner-container p{
            font-size: 12pt;
        }
    }

    @media screen and (max-width: 390px){
        #banner-container h2{
            font-size: 32pt;
        }

        #banner-container p{
            font-size: 12pt;
        }
    }
</style>