<script>
    import { onMount} from "svelte";
    import { useNavigate, useLocation } from "svelte-navigator";
    import {push, pop, replace} from 'svelte-spa-router'
    
    const navigate = useNavigate();
    const location = useLocation();
  
    $: console.log($location);
    let username;
    let password;
    let csrfToken;
    let isAuthenticated = true;
    let submitted = false;
    let authUserName;

    onMount(() => {
      fetch("/api/getsession", {
        credentials: "same-origin",
      })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        if (data.login == true) {
          isAuthenticated = true;
          authUserName = data.username
        } else {
          isAuthenticated = false;
          csrf();
        }
      })
      .catch((err) => {
        console.log(err);
      });
    });
  
    const csrf = () => {
      fetch("/api/getcsrf", {
        credentials: "same-origin",
      })
      .then((res) => {
        csrfToken = res.headers.get(["X-CSRFToken"]);
        // console.log(csrfToken);
      })
      .catch((err) => {
        console.log(err);
      });
    }
  
    const login = () => {
      
      console.log(username) //username is undefined in case of mozila
      console.log(password)
      if (username == null || username == "" || password == null || password == ""){
        alert("Input data are not correct!")
        return;
      }
      fetch("/api/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken
        },
        credentials: "same-origin",
        body: JSON.stringify({ username: username, password: password }),
      })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        if (data.login == true) {
          isAuthenticated = true;
          authUserName = username;
        }
        else{
          alert("User doesn't exist!")
        }
      })
      .catch((err) => {
        alert("Connection error!")
      });
    }
  
    const manageAccount = () => {
      
    };
  
    const logout = () => {
      fetch("/api/logout", {
        credentials: "same-origin",
      })
      .then(() => {
        isAuthenticated = false;
        csrf();
      })
      .catch((err) => {
        console.log(err);
      });
    };
  </script>
  
  <style>
    .container {
      padding-top: 5%;
    }
    .submitted input:invalid {
		  border: 1px solid #c00;
	  }
    
  </style>
  
  <center>
    <div class="container">
      <div class="row">
        <div class="col-md-8 offset-md-2" tabindex={0}>
          {#if isAuthenticated}
            <h1 tabindex={2}>You are {authUserName}</h1>
            <br/><br/>
            <button class="btn btn-success" type="button"  on:click={()=>navigate("/profile",{replace:"false"})}>Account Management</button>
            &nbsp;&nbsp;&nbsp;
            <button class="btn btn-danger" type="button" on:click={logout}>logout</button>
          {:else}
          
          <h1>Log In</h1><br/>
            <form id="form" class:submitted >
              
              <div class="form-group row">
                <div class="col-md-4 offset-md-2"><label for="username">Username :</label> </div>
                <div class="col-md-4"><input type="text" tabindex={3} bind:value={username}  class="form-control"  placeholder="Enter username"   required /></div>
              </div>
              <br />
              
              <div class="form-group row">
                <div class="col-md-4 offset-md-2"><label for="username">Password :</label> </div>
                <div class="col-md-4"><input type="password" bind:value={password} class="form-control"  placeholder="Enter password" required /></div>
              </div>
              <br /><br />
              <div class="form-group ">
              <button type="button" tabindex={0} class="btn btn-primary" on:click={login}>Login</button>
              &nbsp;&nbsp;&nbsp;&nbsp;
              <button type="button" class="btn btn-secondary" on:click={()=>navigate("/register",{replace:"false"})}>Go to Register</button>
            </div>
            </form>

            
          {/if}
        </div>
      </div>
    </div>

  </center>
  