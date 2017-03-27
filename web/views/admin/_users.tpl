<div>
    <br/>
    <h4 class="text-muted"> Registered Users </h4>
    <div class="pull-right"> <a class="btn btn-sm btn-info" href="/admin/create_user">Add New User</a></div>
    <br/>    
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
                    <form method="post" action="/admin/delete_user">
                    <input type="hidden" name="username" value="{{user[0]}}" />
                    <th scope="row">{{user[0]}}</th>
                    <td>{{user[1]}}</td>
                    <td>{{user[2]}}</td>
                    <td><button class="btn btn-sm btn-secondary" type="submit">Delete</button></td>
                    </form>
                </tr>
                % end
            </tbody>
        </table>
    <p>
</div>