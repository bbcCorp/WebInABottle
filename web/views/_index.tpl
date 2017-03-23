
<div>
    <h3> {{page_header}} </h3>
    <p>
        Here's a list of functionalities that this app provides
        <ul class="list-group">
            % for func in contentLst:
                <li class="list-group-item">{{func}}</li>
            % end
        </ul>
    <p>
</div>