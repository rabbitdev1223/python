<script>
	//Imports for used svelte components
	import { onMount} from "svelte";
	import Modal from "./components/Modal.svelte"
	import Header from "./components/Header.svelte";
	import Banner from "./components/Banner.svelte";
	import ContentHolder from "./components/ContentHolder.svelte";
	import Footer from "./components/Footer.svelte";
	import {csrfToken} from './store.js';

	//Boolean which determines if the user is logged in or not.
	let userLoggedIn = false;
	
	//Boolean which determines if the login/signup modal is showing
	let showModal = false;

	//An array of strings which signify different modal views
	let possibleModalViews = ["login-view","signup-view"];
	//The currently selected modal view
	let currentModalView = possibleModalViews[1];
	//The title value of the current modal view
	let currentModalTitle = "";

	//Boolean which determines if there is an error message on the login/signup modal.
	let showErrorMessage = false;
	//The current error message displayed on the modal.
	let currentErrorMessage = "Example Error";

	//Function which opens the login/sign modal to the specified modal view
	const openModal = (modalView) => {
		currentModalView = modalView;
		
		if(modalView == "login-view"){
			currentModalTitle = "Login";
		}else if(modalView == "signup-view"){
			currentModalTitle = "Signup";
		}

		showModal = true;
	}
	
	onMount(() => {
	  
		csrf();

      fetch("/api/getsession", {
        credentials: "same-origin",
      })
      .then((res) => res.json())
      .then((data) => {
        
        if (data.login == true) {
			userLoggedIn = true;
          	
        } else {
			userLoggedIn = false;
          
        }
      })
      .catch((err) => {
        console.log(err);
      });
    });

	//Functions which turns off the login/signup modal also turns off error message if there is any.
	const closeModal = () => {
		showModal = false;
		if(showErrorMessage)showErrorMessage = false
	}

	const csrf = () => {
      fetch("/api/getcsrf", {
        credentials: "same-origin",
      })
      .then((res) => {
        csrfToken.set(res.headers.get(["X-CSRFToken"]));
        // console.log(csrfToken);
		// console.log($csrfToken);
		
      })
      .catch((err) => {
        console.log(err);
      });
    }
	
	
	const logout = () => {
      fetch("/api/logout", {
        credentials: "same-origin",
      })
      .then(() => {
        userLoggedIn = false;
        csrf();
      })
      .catch((err) => {
        console.log(err);
		
      });
    };
	//Function which is called when the user tries to login in
	const loginRequested = (e) =>{
		//Takes the information from the login request and creates a new FormData object which puts the info into an array of key, value pairs
		const formData = new FormData(e.target);
		
		//Object to store parsed form data
		let userInfo = {email: "", password: ""};

		/*For loop which runs through all key value pairs sent from the login request.
		  If the key of the current value is 'user-email' the email value of the 'userInfo' variable
		  is set to that keys value, same goes for the 'user-password'*/ 
		for (const [k, v] of formData.entries()) {
			if(k == "user-email"){
				userInfo.email = v;
			}else if(k == "user-password"){
				userInfo.password = v;
			}
		}

		//All fetch request expect a response in the following JSON format { status: "ok/error", message: "response message"}


		/*Makes a fetch request to the login route of the backend server, and sends over the recieved form data
		  over in JSON format using JSON.stringify. After the response is recieved we check the status of the response
		  through the 'status' value, we also use the 'message' value to display the correct message when there is an
		  error. If the request is successful when close the login/signup modal and log the user in, otherwise we display
		  an error message*/
		fetch('/api/login',{
			method: 'POST',
			mode: 'cors',
			credentials: 'same-origin',
			headers:{
				'Content-Type': 'application/json',
				'Access-Control-Allow-Origin': '*',
				"X-CSRFToken": $csrfToken
			},
			body: JSON.stringify(userInfo)
		})
		.then(res => res.json())
		.then(resJson => {
			if(resJson.status == "error"){
				if(resJson.message == "invalid-login-request"){
					currentErrorMessage = "Invalid login request"
				}else if(resJson.message == "invalid-login-fields"){
					currentErrorMessage = "You must fill in all required fields"
				}
				showErrorMessage = true;
			}else if(resJson.status == "ok"){
				closeModal();
				userLoggedIn = true;
			}
		})
		.catch(error => {
			console.error(error);
			currentErrorMessage = "Error Connection!";
			showErrorMessage = true;
		});
	}
	

	//Function which is called when the user tries to signup
	const signupRequested = (e) =>{
		//Takes the information from the signup request and creates a new FormData object which puts the info into an array of key, value pairs
		const formData = new FormData(e.target);
		//Object to store parsed form data
		let userInfo = {email: "", password: "", password_confirm: ""};

		/*For loop which runs through all key value pairs sent from the signup request.
		If the key of the current value is 'user-email' the email value of the 'userInfo' variable
		is set to that keys value, same goes for the 'user-password' and 'user-password-confirm'*/ 
		for (const [k, v] of formData.entries()) {
			if(k == "user-email"){
				userInfo.email = v;
			}else if(k == "user-password"){
				userInfo.password = v;
			}else if(k == "user-password-confirm"){
				userInfo.password_confirm = v;
			}
		}
		//validation
		if (userInfo.password != userInfo.password_confirm){
			currentErrorMessage = "Passwords don't match";
			showErrorMessage = true;
			return;
		}
		if (userInfo.email.length < 1){
			currentErrorMessage = "Email is required!";
			showErrorMessage = true;
			return;
		}
		if (userInfo.password.length < 3){
			currentErrorMessage = "Password must be 3 characters long";
			showErrorMessage = true;
			return;
		}
		
		/*Makes a fetch request to the signup route of the backend server, and sends over the recieved form data
		over in JSON format using JSON.stringify. After the response is recieved we check the status of the response
		through the 'status' value, we also use the 'message' value to display the correct message when there is an
		error. If the request is successful we open the login modal view, otherwise we just display an error message*/
		fetch('api/signup',{
			method: 'POST',
			mode: 'cors',
			credentials: 'same-origin',
			headers:{
				'Content-Type': 'application/json',
				'Access-Control-Allow-Origin': '*',
				"X-CSRFToken": $csrfToken
			},
			body: JSON.stringify(userInfo)
		})
		.then(res => res.json())
		.then(resJson => {
			if(resJson.status == "error"){
				
				currentErrorMessage = resJson.message;
				showErrorMessage = true;
			}else if(resJson.status == "ok"){
				openModal(possibleModalViews[0]);
			}
		})
		.catch(error => {
			console.log(error);
			currentErrorMessage = "Error Connection!";
			showErrorMessage = true;
		});
	}
</script>

<main>
	<!--Shows login/signup modal only if 'showModal' is true-->
	{#if showModal}
		<!--Login/Signup Modal Svelte Component-->
		<Modal modalTitleText={currentModalTitle} on:click={()=>{closeModal();}}>
			<!--Modal Slot with stop propagation(don't click through elements)-->
			<div slot="modal-slot" on:click={(e)=>{e.stopPropagation();}}>
				{#if currentModalView == possibleModalViews[0]} <!--Login View-->
					<form class="centered-form" on:submit|preventDefault={loginRequested}>
						<input type="email" name="user-email" class="form-input" placeholder="Email (Required)" required>
						<input type="password" name="user-password" class="form-input" placeholder="Password (Required)" required>
						<button type="submit" class="form-button">Login</button>
					</form>
					{#if showErrorMessage == true}
						<p class="response-error">{currentErrorMessage}</p>
					{/if}
				{:else if currentModalView == possibleModalViews[1]} <!--Signup View-->
					<form class="centered-form" on:submit|preventDefault={signupRequested}>
						<input type="email" name="user-email" class="form-input" placeholder="Email (Required)" required>
						<input type="password" name="user-password" class="form-input" placeholder="Password (Required)" required>
						<input type="password" name="user-password-confirm" class="form-input" placeholder="Repeat Password (Required)" required> 
						<button type="submit" class="form-button">Signup</button>
					</form>
					{#if showErrorMessage == true}
						<p class="response-error">{currentErrorMessage}</p>
					{/if}
				{/if}
			</div>
		</Modal>
	{/if}

	<!--Header svelte componenet which has exposed variables for logoPath, userLoggedIn which is set to the variable of the same
	name which is controlled locally. Header also has function listeners for login requests, signup requests, logout requests, and
	account requests-->
	<Header headerLogoPath="assets/white_transparent.png" userLoggedIn={userLoggedIn}
	on:loginRequested={()=>{openModal(possibleModalViews[0]);}}
	on:signupRequested={()=>{openModal(possibleModalViews[1]);}}
	on:logoutRequested={()=>{logout()}}
	on:accountRequested={()=>{console.log("Account")}}></Header>

	<!--Site banner/welcome svelte component (Only shown when user isn't logged in)-->
	{#if userLoggedIn == false}
		<Banner></Banner>
	{/if}
	<!--Svelte component which contains multiple other svelte components and also has 3 slots for more simplier content expansion, 
		also takes in whether or not the user is logged in-->
	<ContentHolder userLoggedIn={userLoggedIn}>
		<!--Slot content is displayed after internal ContentHolder content-->
		<div slot="content-slot-one">

		</div>
		<div slot="content-slot-two">

		</div>
		<div slot="content-slot-three">

		</div>
	</ContentHolder>

	<!--Footer svelte componenet which simply has copyright text which appears at the bottom of the page.-->
	<Footer></Footer>
</main>

<style>

</style>