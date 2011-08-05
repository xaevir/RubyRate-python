<%inherit file="/base.mako"/>
<%def name="page_name()">quote</%def>

<form action="${save_url}" method="post">

    <label>Name</label>
    <input name="name" type="text"/>

    <label>Email</label>
    <input name="email" type="text"/>

    <label>Product</label>
    <input name="product" type="text"/>

    <label>Product Specs</label>
    <input name="specs" type="text"/>

    <label>Quantity</label>
    <input name="quantity" type="text"/>

    <label>Lead time</label>
    <input name="lead_time" type="text"/>

    <label>Shipping destination</label>
    <input name="shipping_destination" type="text"/>

    <label>Payment terms</label>
    <input name="payment_terms" type="text"/>

    <input type="submit" name="submit" 
           class="button" value="Submit"/>
</form>	
