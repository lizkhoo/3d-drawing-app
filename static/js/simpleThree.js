var balls = [];
	var done = false;

	var container = document.getElementById(divID);
	//console.log(container);

	var renderer = new THREE.WebGLRenderer({antialias:true});
	renderer.setSize( 200, 200 );

	container.appendChild(renderer.domElement);

	var scene = new THREE.Scene();

	var camera = new THREE.OrthographicCamera( -500,500,-500,500,100,10000);

	camera.position.set( 0, 0,1000 );
	camera.lookAt( scene.position );

	var geometry = new THREE.SphereGeometry( 25, 12, 12 );

	var material = new THREE.MeshLambertMaterial( { color: 0xFFffff } );
	var mesh = new THREE.Mesh( geometry, material );

	mesh.updateMatrix();
	mesh.matrixAutoUpdate = true;

	var light = new THREE.DirectionalLight( 0xFFFFff );
	light.position.set( 1, -1, 1 );
	scene.add( light );

	var light = new THREE.DirectionalLight( 0x555555 );
	light.position.set( 0, 0, -1 );
	scene.add( light );

	var light = new THREE.DirectionalLight( 0xFFFFff );
	light.position.set( -1, 1, 1 );
	scene.add( light );
	//addBalls();
	//console.log(scene);

	var geometry = new THREE.Geometry();
	geometry.name = "Liz_Line";
	var vertString = "{{ design.design }}" || "";
	var verts = vertices.split(",");

	for(var i = 0 ; i < verts.length ; i +=3){
		if(verts[i])
		geometry.vertices.push(new THREE.Vector3(parseFloat(verts[i])||0,parseFloat(verts[i+1])||0,parseFloat(verts[i+2])||0));
	}

	var curve = new THREE.SplineCurve3(geometry.vertices);
	var geo = new THREE.TubeGeometry(curve, geometry.vertices.length*2, 5, 3, closed);
	var tubeMesh = new THREE.Mesh(geo,new THREE.MeshLambertMaterial({color: 0xffffff}));

	scene.add(tubeMesh);

	draw();
		
	function draw(){

		renderer.render( scene, camera );
	}