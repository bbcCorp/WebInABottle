<div>
    <br/>
    <h4 class="text-muted"> Create User </h4>
    <br/>
    % if err_msg:
       <label class="text-alert">{{err_msg}}</label> 
    % end
    <form class="" method="post" action="/admin/create_role">

        <div class="form-group">
            <label for="name" class="cols-sm-2 control-label">Role Name</label>
            <div class="cols-sm-10">
                <div class="input-group">
                    <span class="input-group-addon"><i class="fa fa-user fa" aria-hidden="true"></i></span>
                    <input type="text" class="form-control" name="role" id="role"  placeholder="Role Name"/>
                </div>
            </div>
        </div>

        <div class="form-group">
            <label for="level" class="cols-sm-2 control-label">Role Level</label>
            <div class="cols-sm-10">
                <div class="input-group">
                    <span class="input-group-addon"><i class="fa fa-envelope fa" aria-hidden="true"></i></span>
                    <input type="text" class="form-control" name="level" id="level"  placeholder="Enter Level"/>
                </div>
            </div>
        </div>

        <div class="form-group ">
            <button class="btn btn-lg btn-primary btn-block" type="submit">Create Role</button>
        </div>

    </form>

</div>