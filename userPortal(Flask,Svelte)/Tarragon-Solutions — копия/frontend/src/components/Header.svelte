<script>
    //Imports the Modal svelte component
    import Modal from './Modal.svelte'

    //Svelte function for dispatching custom events
    import {createEventDispatcher} from 'svelte';
    const dispatch = createEventDispatcher();

    //Expose variable to the path of the header logo
    export let headerLogoPath;
    
    //An array of objects which signify the links inside the menu bar.
    export let headerLinks=[{text: "Home", href: "#top"}, 
                            {text: "Mission Statement", href: "#mission-statement"}, 
                            {text: "Contact", href: "#contact-container"}];

    //Exposed variable to determine if user is logged in or not.
    export let userLoggedIn = false;

    //Boolean which determines if the mobile modal menu show be shown.
    let showMobileMenu = false;

    //Custom dispatch funtions for the account interation on the header, each dispatch will close the mobile menu.
    const loginRequested = () =>{
        closeMobileMenu();
        dispatch("loginRequested");
    }

    const signupRequested = () =>{
        closeMobileMenu();
        dispatch("signupRequested");
    }

    const accountRequested = () =>{
        closeMobileMenu();
        dispatch("accountRequested");
    }

    const logoutRequested = () =>{
        closeMobileMenu();
        dispatch("logoutRequested");
    }


    //Functions for opening and closing the mobile menu modal
    const openMobileMenu = () => {
        showMobileMenu = true;
    }

    const closeMobileMenu = () => {
        showMobileMenu = false;
    }

</script>

<!--Mobile Menu Modal (Will only show if 'showMobileMenu' is set to true)-->
{#if showMobileMenu == true}
<Modal modalTitleText="">
    <div id="modal-slot" slot="modal-slot" on:click={()=>{closeMobileMenu()}}>
        <!--Creates links for each of the menu items specified in the 'headerLinks' array-->
        <ul class="mobile-menu-list" on:click={(e)=>{e.stopPropagation();}}>
            {#each headerLinks as link}
                <li><a href={link.href} on:click={()=>
                {closeMobileMenu()}}>{link.text}</a></li>
            {/each}
        </ul>

        <!--Buttons for account management. Manage account/logout are only visible when the user
        is logged in, and login/signup are only visible when the user isn't logged in.-->
        {#if userLoggedIn}
            <button class="user-account-mobile-button" on:click|preventDefault={accountRequested}>Manage Account</button>
            <button class="user-account-mobile-button" on:click|preventDefault={logoutRequested}>Logout</button>
        {:else}
            <button class="user-account-mobile-button" on:click|preventDefault={loginRequested}>Login</button>
            <button class="user-account-mobile-button" on:click|preventDefault={signupRequested}>Signup</button>
        {/if}
    </div>
</Modal>
{/if}

<header id="top">
    <img src={headerLogoPath} alt="Header Logo">

    <!--Creates links for each of the menu items specified in the 'headerLinks' array-->
    <ul class="menu-list">
        {#each headerLinks as link}
            <li><a href={link.href}>{link.text}</a></li>
        {/each}
    </ul>


    <!--Buttons for account management. Manage account/logout are only visible when the user
    is logged in, and login/signup are only visible when the user isn't logged in.-->
    <div id="user-account-container">
        {#if userLoggedIn}
             <button class="user-account-button" on:click|preventDefault={accountRequested}>Manage Account</button>
             <button class="user-account-button" on:click|preventDefault={logoutRequested}>Logout</button>
        {:else}
            <button class="user-account-button" on:click|preventDefault={loginRequested}>Login</button>
            <button class="user-account-button" on:click|preventDefault={signupRequested}>Signup</button>
        {/if}
    </div>

    <!--Mobile Menu 'hamburger' icon, only visible when screen is smaller than 820px-->
    <img class="mobile-menu-icon" src="assets/hamburger_menu.png" alt="mobile-menu" on:click={openMobileMenu}>
</header>

<style>
    /*Header container styling*/
    header{
        display: grid;
        grid-template-columns: minmax(100px, 140px), 3fr, minmax(40px, 80px);
        width: auto;
        height: auto;
        padding: 16px;
        top: 0px;
        left: 0px;
        background-color: var(--document-secondary-background-color);
        color: var(--document-header-text-color);
    }

    /*Header logo image styling*/
    header img{
        grid-column: 1;
        max-width: auto;
        max-height: 120px;
        margin-left: 60px;
    }

    /*Mobile menu modal styling*/
    #modal-slot{
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        width: 100%;
        height: 100%;
    }

    /*Header menu list container styling*/
    .menu-list{
        width: auto;
        height: auto;
        grid-column: 2;
        margin-top: 46px;
        margin-right: 40px;
        list-style-type: none;
        overflow: hidden;
    }

    /*Header menu list items styling*/
    .menu-list li{
        display: inline-block;
        display: inline;
        margin: 0px 12px;
        font-size: 15pt;
    }

    /*Header menu list items link styling*/
    .menu-list li a{
        color: var(--document-header-text-color);
        text-decoration: none;
        transition: color 0.4s;
    }

    /*Header menu list items link hover styling*/
    .menu-list li a:hover{
        color: var(--document-header-link-hover-color);
    }

    /*User account controls conatiner styling*/
    #user-account-container{
        grid-column: 3;
        display: flex;
        justify-content: center;
        width: auto;
    }

    /*User account buttons styling*/
    .user-account-button{
        background-color: var(--document-secondary-background-color);
        color: var(--document-header-text-color);
        border: none;
        padding: 0px 8px;
        font-size: 14pt;
        transition: color 0.4s;
    }

    /*User account buttons hover styling*/
    .user-account-button:hover{
        color: var(--document-header-link-hover-color);
    }

    /*Mobile Menu List Container Styling*/
    .mobile-menu-list{
        grid-column: 2;
        list-style-type: none;
        overflow: hidden;
        text-align: center;
    }

    /*Mobile menu list item styling*/
    .mobile-menu-list li{
        margin: 0px 12px;
        font-size: 18pt;
    }

    /*Mobile menu list item link styling*/
    .mobile-menu-list li a{
        color: var(--document-header-text-color);
        text-decoration: none;
        transition: color 0.4s;
    }

    /*Mobile menu list item link hover styling*/
    .mobile-menu-list li a:hover{
        color: var(--document-header-link-hover-color);
    }

    /*Mobile account buttons styling*/
    .user-account-mobile-button{
        width: 200px;
        height: auto;
        background-color: var(--form-button-normal-background-color);
        color: var(--document-header-text-color);
        border: none;
        border-radius: var(--form-button-border-radius);
        padding: 0px 8px;
        font-size: 14pt;
        margin: 6px 0px;
        transition: background-color 0.4s;
    }

    /*Mobile account buttons hover styling*/
    .user-account-mobile-button:hover{
        background-color: var(--form-button-hover-background-color);
    }

    /*Mobile menu 'hamburger' button styling*/
    .mobile-menu-icon{
        display: none;
        grid-column: 3;
        width: 48px;
        height: 48px;
        margin-top: 40px;
        margin-left:480px;
    }

    /*Mobile Styling*/
    @media screen and (max-width: 700px){
        .mobile-menu-icon{
            margin-left:400px;
        }
    }

    @media screen and (max-width: 690px){
        .mobile-menu-icon{
            margin-left:300px;
        }

        header img{
            margin-left: 20px;
        }
    }

    @media screen and (max-width: 470px){
        .mobile-menu-icon{
            margin-left:200px;
        }

        header img{
            margin-left: 20px;
        }
    }

    @media screen and (max-width: 360px){
        .mobile-menu-icon{
            margin-left:140px;
        }

        header img{
            margin-left: 10px;
        }
    }

    @media screen and (max-width: 820px){
        #user-account-container{
            display: none;
        }

        header ul{
            display: none;
        }

        .mobile-menu-icon{
            display: block;
        }
    }
</style>