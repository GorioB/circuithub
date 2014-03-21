//handles manual upload
var types = ['RLC', 'BJT', 'Diode']
var row = 0;
var subtypes = {	"RLC" : ['Resistor', 'Inductor', 'Capacitor'],
					"BJT" : ['NPN', 'PNP'],
					"Diode" : ['1n4008', '1n2345'],
				};



var subtype = "";
var pricelist;

$.getJSON('pricelist', function(jd){
	console.log('here');
	pricelist = JSON.parse(jd);
	
	var i;
	for(i = 0; i < pricelist.length; i++){
		
		
	}
	
	
	
	
	
});



$(function(){
	console.log("ready");
		
	$('#addItemBtn').on('click', function(){
		row++;
		
		$('#maxrow').val(row);
		
		var element;
		element = "<tr><td><select class='input c-type r" + row + "' name='c-type-" + row + "' id='c-type-" + row + "'><option value='' disabled selected>Type</option>";
		var i;
		for(i = 0 ; i < types.length; i++){
			element += "<option value='" + types[i] + "'>" + types[i] + "</option>";
		}
		element += "</select></td></tr>";
		
		
		$('#itemsList tr:last').before(element);
		
	});
	
});


$(document).on('change', '.c-type', function(){
	var sel = $(this).val();
	var this_id = $(this).attr('id');
	
	var tokens = this_id.split('-');
	var this_row = tokens[2];
	
	var element;
	
	var childtype = (sel == 'Diode') ? 'c-val' : 'c-subtype';
	var childoption = (sel == 'Diode') ? 'Model' : 'Subtype';
	element = "<td><select class='input " + childtype + " r" + this_row + "' name='" + childtype + "-" + this_row + "' id='" + childtype + "-" + this_row + "'><option value='' disabled selected>" + childoption +"</option>";
	var i;
	for(i = 0 ; i < subtypes[sel].length; i++){
		element += "<option value='" + subtypes[sel][i] + "'>" + subtypes[sel][i] + "</option>";
	}
	element += "</select></td>";	
	
	removeRight('c-type-' + this_row);
	$(this).parent().parent().append(element);

});

/*
$(document).on('click', '#submitBtn', function(){
	$('manualForm').


});
*/
$(document).on('change', '.c-subtype', function(){
	var sel = $(this).val();
	var this_id = $(this).attr('id');
	//console.log('>>>inchange ' + this_id +' to ' + sel);
	
	var tokens = this_id.split('-');
	var this_row = tokens[2];
	
	var element = "<td>";
	
	switch($('#c-type-' + this_row).val()){
		case "RLC":
			element += "<input type='text' placeholder='Value (i.e. 10k, 0.023)' class='input c-val r" + this_row + "' name='c-val-" + this_row + "' id='c-val-" + this_row + "' />";
			break;
		case "BJT":
			element += "<input type='text' placeholder='Model (i.e. 2N3904, etc.)' class='input c-val r" + this_row + "' name='c-val-" + this_row + "' id='c-val-" + this_row + "' />";
			break;
	}
	
	element += "</td>";
	removeRight('c-subtype-' + this_row);
	$(this).parent().parent().append(element);
});



$(document).on('click', '.c-val', function(){
	var sel = $(this).val();
	var this_id = $(this).attr('id');
	//console.log('>>>inchange ' + this_id +' to ' + sel);
	
	var tokens = this_id.split('-');
	var this_row = tokens[2];
	
	var element = "<td><input type='text' placeholder='Quantity' class='input c-qty r" + this_row + "' name='c-qty-" + this_row + "' id='c-qty-" + this_row + "' /></td>";

	//removeRight('c-val-' + this_row);
	if ( $('#c-qty-' + this_row).length == 0)
		$(this).parent().parent().append(element);
});


function removeRight(c_id){ //on select change, remove the elements to the right
	//cid : c-type-row#
	var tokens = c_id.split('-');
	//console.log('received id: ' + tokens[1]);
	
	switch (tokens[1]){
		case 'type': $('#c-subtype-' + tokens[2]).parent().remove();
		case 'subtype': $('#c-val-' + tokens[2]).parent().remove(); 
			$('#c-qty-' + tokens[2]).parent().remove();
	}
	
}


