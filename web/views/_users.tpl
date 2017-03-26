<div>
    <br/>
    <h4 class="text-muted"> Registered Users </h4>
    <br/>
    <div class="pull-right"> <a href="/register">Register New User</a></div>
    <p>
        <table class="table table-hover">
            <thead class="thead-inverse">
                <tr>
                    <th>UserID</th>
                    <th>Role</th>
                    <th>Email</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                % for user in users:
                <tr>
                    <th scope="row">{{user[0]}}</th>
                    <td>{{user[1]}}</td>
                    <td>{{user[2]}}</td>
                    <td></td>
                </tr>
                % end
            </tbody>
        </table>
    <p>
</div>