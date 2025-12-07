# Fix room_management.html addRoom function
with open('templates/rooms/room_management.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add the addRoom and action handler functions before the closing script tag
fix = """
// Action handlers
function addRoom() {
    window.location.href = '{% url "rooms:room-create" %}';
}

async function editRoom(id, currentStatus) {
    const statuses = ['dispo', 'reserved', 'booked', 'maintenance'];
    const currentIndex = statuses.indexOf(currentStatus);
    const nextIndex = (currentIndex + 1) % statuses.length;
    const newStatus = statuses[nextIndex];
    const statusNames = {'dispo':'Available','reserved':'Reserved','booked':'Booked','maintenance':'Maintenance'};
    
    if (!confirm(`Change room #${id} from ${statusNames[currentStatus]} to ${statusNames[newStatus]}?`)) return;
    
    try {
        const r = await fetch(`/api/rooms/reception/${id}/status/`, {
            method: 'PATCH',
            headers: {'Content-Type':'application/json','X-CSRFToken':document.querySelector('[name=csrfmiddlewaretoken]').value},
            credentials: 'same-origin',
            body: JSON.stringify({status: newStatus})
        });
        if (r.ok) { alert('Status updated!'); fetchRooms(); } else { alert('Error: ' + (await r.json()).error); }
    } catch(e) { alert('Error: ' + e); }
}

async function deleteRoom(id) {
    if (!confirm(`Delete room #${id}? This action cannot be undone.`)) return;
    alert('Delete functionality not yet implemented.');
}

// Initialize room management page"""

content = content.replace(
    "// Initialize room management page",
    fix
)

# Add onclick to Add Room button
content = content.replace(
    '<button type="button" class="ml-3 inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">',
    '<button onclick="addRoom()" class="ml-3 inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">'
)

# Add onclick to action buttons  
content = content.replace(
    '<button class="text-blue-600 hover:text-blue-900 mr-3">Edit</button>',
    '<button onclick="editRoom(${room.id}, \'${room.status}\')" class="text-blue-600 hover:text-blue-900 mr-3">Edit Status</button>'
)
content = content.replace(
    '<button class="text-red-600 hover:text-red-900">Delete</button>',
    '<button onclick="deleteRoom(${room.id})" class="text-red-600 hover:text-red-900">Delete</button>'
)

with open('templates/rooms/room_management.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed!")
