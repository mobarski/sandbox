from bottle import route, run, request, template, static_file, redirect
import kcal

html_form = """
<center>
<form action="{{action}}" method="post" >
	<br>
	<textarea name="text" style="height:300px"></textarea>
	<br>
	<input type="submit" value="{{label}}" style="width:100px">
</form>
</center>
"""

tab_out = """
<center>
<h1>razem: {{data[-1][2]}} kcal <br><small>{{data[-1][1]}} gram</small></h1>
<!--<h1>Razem: {{data[-1][2]}} kcal</h1>
<p><small>{{data[-1][1]}} gram</small></p>-->
<p><small>{{int(100*data[-1][2]/max(1,data[-1][1]))}} kcal/100g</small></p>
<table>
	<tr>
		<th>nazwa</th><th>gramy</th><th>kcal</th>
	</tr>
	% for item,weight,kcal in data[:-1]:
		<tr>
			<td>{{item}}</td>
			<td>{{weight}}</td>
			<td>{{kcal}}</td>
		</tr>
	% end
</table>
</center>
"""

########################################

@route('/')
def main():
	return template(html_form,action='/',label='licz')

@route('/',method='POST')
def main_post():
	text = request.forms.text
	if not text: redirect('/')
	kcal_list = kcal.licz(text)
	out = template(tab_out,data=kcal_list)
	return out

@route('/add')
def main():
	return template(html_form,action='/add',label='dodaj')

@route('/add',method='POST')
def main_post():
	text = request.forms.text
	return "TODO"

@route('/db')
def static():
	return static_file('kcal.txt',root=".")

run(host='0.0.0.0',port=9090)
