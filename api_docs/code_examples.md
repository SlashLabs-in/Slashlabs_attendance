# API Code Examples

This document provides code examples for interacting with the SlashLabs Attendance System API in different programming languages.

## Authentication

### Login

#### cURL

```bash
curl -X POST 'https://your-domain.com/api/login' \
-H 'Content-Type: application/json' \
-d '{
    "username": "employee1",
    "password": "password123"
}'
```

#### JavaScript (Fetch)

```javascript
const loginUser = async (username, password) => {
  try {
    const response = await fetch("https://your-domain.com/api/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username,
        password,
      }),
    });

    if (!response.ok) {
      throw new Error("Login failed");
    }

    const data = await response.json();
    localStorage.setItem("token", data.token);
    return data;
  } catch (error) {
    console.error("Error:", error);
  }
};
```

#### Python (Requests)

```python
import requests

def login_user(username, password):
    url = 'https://your-domain.com/api/login'
    payload = {
        'username': username,
        'password': password
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        data = response.json()
        token = data['token']
        return token
    else:
        print(f"Login failed: {response.text}")
        return None
```

#### Swift

```swift
func login(username: String, password: String, completion: @escaping (Result<String, Error>) -> Void) {
    let url = URL(string: "https://your-domain.com/api/login")!
    var request = URLRequest(url: url)
    request.httpMethod = "POST"
    request.addValue("application/json", forHTTPHeaderField: "Content-Type")

    let body: [String: Any] = [
        "username": username,
        "password": password
    ]

    request.httpBody = try? JSONSerialization.data(withJSONObject: body)

    URLSession.shared.dataTask(with: request) { data, response, error in
        if let error = error {
            completion(.failure(error))
            return
        }

        guard let data = data else {
            completion(.failure(NSError(domain: "No data", code: 0)))
            return
        }

        do {
            if let json = try JSONSerialization.jsonObject(with: data) as? [String: Any],
               let token = json["token"] as? String {
                completion(.success(token))
            } else {
                completion(.failure(NSError(domain: "Invalid response", code: 0)))
            }
        } catch {
            completion(.failure(error))
        }
    }.resume()
}
```

## Attendance

### Check-In

#### cURL

```bash
curl -X POST 'https://your-domain.com/api/attendance/check-in' \
-H 'Authorization: Bearer YOUR_TOKEN_HERE' \
-F 'image=@/path/to/image.jpg' \
-F 'location=Office Building, Floor 3' \
-F 'status=present' \
-F 'notes=Regular check-in'
```

#### JavaScript (Fetch)

```javascript
const checkIn = async (location, status, notes, imageFile) => {
  try {
    const token = localStorage.getItem("token");

    if (!token) {
      throw new Error("Not authenticated");
    }

    const formData = new FormData();
    if (imageFile) {
      formData.append("image", imageFile);
    }

    if (location) {
      formData.append("location", location);
    }

    if (status) {
      formData.append("status", status);
    }

    if (notes) {
      formData.append("notes", notes);
    }

    const response = await fetch(
      "https://your-domain.com/api/attendance/check-in",
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      }
    );

    if (!response.ok) {
      throw new Error("Check-in failed");
    }

    return await response.json();
  } catch (error) {
    console.error("Error:", error);
  }
};
```

#### Python (Requests)

```python
import requests

def check_in(token, location=None, status='present', notes=None, image_path=None):
    url = 'https://your-domain.com/api/attendance/check-in'
    headers = {
        'Authorization': f'Bearer {token}'
    }

    data = {}
    if location:
        data['location'] = location

    if status:
        data['status'] = status

    if notes:
        data['notes'] = notes

    files = {}
    if image_path:
        files['image'] = open(image_path, 'rb')

    response = requests.post(url, headers=headers, data=data, files=files)

    if files and 'image' in files:
        files['image'].close()

    if response.status_code == 201:
        return response.json()
    else:
        print(f"Check-in failed: {response.text}")
        return None
```

### Get Attendance History

#### cURL

```bash
curl -X GET 'https://your-domain.com/api/attendance/history?page=1&per_page=10&start_date=2025-01-01&end_date=2025-12-31' \
-H 'Authorization: Bearer YOUR_TOKEN_HERE'
```

#### JavaScript (Fetch)

```javascript
const getAttendanceHistory = async (
  page = 1,
  perPage = 10,
  startDate = null,
  endDate = null
) => {
  try {
    const token = localStorage.getItem("token");

    if (!token) {
      throw new Error("Not authenticated");
    }

    let url = `https://your-domain.com/api/attendance/history?page=${page}&per_page=${perPage}`;

    if (startDate) {
      url += `&start_date=${startDate}`;
    }

    if (endDate) {
      url += `&end_date=${endDate}`;
    }

    const response = await fetch(url, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error("Failed to get attendance history");
    }

    return await response.json();
  } catch (error) {
    console.error("Error:", error);
  }
};
```

#### Python (Requests)

```python
import requests

def get_attendance_history(token, page=1, per_page=10, start_date=None, end_date=None):
    url = f'https://your-domain.com/api/attendance/history?page={page}&per_page={per_page}'

    if start_date:
        url += f'&start_date={start_date}'

    if end_date:
        url += f'&end_date={end_date}'

    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get attendance history: {response.text}")
        return None
```

## User Profile

### Get Profile

#### cURL

```bash
curl -X GET 'https://your-domain.com/api/users/profile' \
-H 'Authorization: Bearer YOUR_TOKEN_HERE'
```

#### JavaScript (Fetch)

```javascript
const getUserProfile = async () => {
  try {
    const token = localStorage.getItem("token");

    if (!token) {
      throw new Error("Not authenticated");
    }

    const response = await fetch("https://your-domain.com/api/users/profile", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error("Failed to get user profile");
    }

    return await response.json();
  } catch (error) {
    console.error("Error:", error);
  }
};
```

#### Python (Requests)

```python
import requests

def get_user_profile(token):
    url = 'https://your-domain.com/api/users/profile'
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get user profile: {response.text}")
        return None
```

### Update Profile

#### cURL

```bash
curl -X PUT 'https://your-domain.com/api/users/profile' \
-H 'Authorization: Bearer YOUR_TOKEN_HERE' \
-H 'Content-Type: application/json' \
-d '{
    "email": "new.email@example.com",
    "full_name": "Updated Full Name",
    "password": "new_password"
}'
```

#### JavaScript (Fetch)

```javascript
const updateUserProfile = async (email, fullName, password = null) => {
  try {
    const token = localStorage.getItem("token");

    if (!token) {
      throw new Error("Not authenticated");
    }

    const data = {};

    if (email) {
      data.email = email;
    }

    if (fullName) {
      data.full_name = fullName;
    }

    if (password) {
      data.password = password;
    }

    const response = await fetch("https://your-domain.com/api/users/profile", {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error("Failed to update user profile");
    }

    return await response.json();
  } catch (error) {
    console.error("Error:", error);
  }
};
```

#### Python (Requests)

```python
import requests

def update_user_profile(token, email=None, full_name=None, password=None):
    url = 'https://your-domain.com/api/users/profile'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    data = {}
    if email:
        data['email'] = email

    if full_name:
        data['full_name'] = full_name

    if password:
        data['password'] = password

    response = requests.put(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to update user profile: {response.text}")
        return None
```
