<script>

</script>

<div id="mission-statement">
    <!--Header text for mission statement component-->
    <h2>Mission Statement</h2>
    <!--Message text for mission statement component-->
    <p>Tarragon Solutions aims to be cost effective, user friendly, and <br>
    and industry advancing set of services designed for<br>
    medical offices and groups that want to get routine tasks done<br>
    faster and without human error.</p>
</div>

<style>
    /*Mission statement container styling*/
    #mission-statement{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 400px;
        text-align: center;
    }

    /*Mission statement header text styling*/
    #mission-statement h2{
        color: var(--document-text-primary-color);
        font-size: 48pt;
        margin: 8px 0px;
    }

    /*Mission statement message styling*/
    #mission-statement p{
        text-align: center;
        color: var(--document-text-primary-color);
        font-size: 16pt;
    }

    /*Mobile styling*/
    @media screen and (max-width: 630px){
        #mission-statement h2{
            font-size: 40pt;
        }

        #mission-statement p{
            font-size: 12pt;
        }
    }

    @media screen and (max-width: 420px){
        #mission-statement h2{
            font-size: 36pt;
        }

        #mission-statement p{
            font-size: 12pt;
        }
    }

    @media screen and (max-width: 390px){
        #mission-statement h2{
            font-size: 32pt;
        }

        #mission-statement p{
            font-size: 12pt;
        }
    }
</style>