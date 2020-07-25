import io from './socket.io.min.js'


var DashSocket = {
	
	socket: null,

	connect: function() {
		if (DashSocket.socket==null) {
			DashSocket.socket = io.connect();
			DashSocket.socket.on('call', function(data) {
				try {
					DashSocket.change(data);
	  			}
	  			catch(error) {
	  			}
			});
		}
	}, 
	
	disconnect: function() {
		if (DashSocket.socket!=null)
			io.disconnect(true);
	},

    setProps: function(id) {
        var element = document.getElementById(id);
        var key = Object.keys(element).find(key=>key.startsWith("__reactInternalInstance$"));
        var internalInstance = element[key];
        var setProps = internalInstance.return.memoizedProps.setProps;
        if (typeof(setProps)=="undefined")
        	return null;
        else
        	return setProps; 
    },


	change: function(data) {
        var setProps = DashSocket.setProps(data['id']);
        if (setProps!=null)
        	setProps(data['val']);        
	}

}

export {DashSocket};




