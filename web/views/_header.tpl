<div class="header">
    <ul class="nav nav-pills pull-right">
        % if active_page == "login":
            <li data-site-topnav="login"><a href="{{URL_PREFIX}}/login">Login</a></li>
        % else:
            <li data-site-topnav="home"><a href="{{URL_PREFIX}}/foo/index">Home</a></li>
            <li data-site-topnav="admin"><a href="{{URL_PREFIX}}/admin/">Admin</a></li>
            <li data-site-topnav="logout"><a href="{{URL_PREFIX}}/logout">Logout</a></li>
        % end
    </ul>
    <h2 class="appTitle">Web in a Bottle</h2>
</div>