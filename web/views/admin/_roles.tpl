<div>
    <br/>
    <h4 class="text-muted"> Application Roles </h4>
    <div class="pull-right"> <a class="btn btn-sm btn-info" href="/admin/create_role">Add New Role</a></div>
    <br/>
    <p>
        <table class="table table-hover">
            <thead class="thead-inverse">
                <tr>
                    <th>RoleID</th>
                    <th>Role</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                % for role in roles:
                <tr>
                    <form method="post" action="/admin/delete_role">
                    <input type="hidden" name="role" value="{{role[0]}}" />                
                    <th scope="row">{{role[1]}}</th>
                    <td>{{role[0]}}</td>
                    <td><button class="btn btn-sm btn-secondary" type="submit">Delete</button></td>
                    </form>
                </tr>
                % end
            </tbody>
        </table>
    <p>
</div>