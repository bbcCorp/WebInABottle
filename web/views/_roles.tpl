<div>
    <br/>
    <h4 class="text-muted"> Application Roles </h4>
    <br/>
    <p>
        <table class="table">
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
                    <th scope="row">{{role[1]}}</th>
                    <td>{{role[0]}}</td>
                    <td></td>
                </tr>
                % end
            </tbody>
        </table>
    <p>
</div>