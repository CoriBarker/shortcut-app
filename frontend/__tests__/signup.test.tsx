import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import SignUp from '../app/signup/page'
import '@testing-library/jest-dom'

// Mock the next/navigation module
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: jest.fn(),
  }),
}))

// Mock the fetch function
global.fetch = jest.fn()

describe('SignUp Page', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks()
  })

  it('renders signup form', () => {
    render(<SignUp />)
    
    // Check if all form elements are present
    expect(screen.getByPlaceholderText(/username/i)).toBeInTheDocument()
    expect(screen.getByPlaceholderText(/email address/i)).toBeInTheDocument()
    expect(screen.getByPlaceholderText(/password/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /sign up/i })).toBeInTheDocument()
  })

  it('handles successful signup', async () => {
    // Mock successful API response
    ;(global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({
        id: 1,
        email: 'test@example.com',
        username: 'testuser'
      })
    })

    render(<SignUp />)
    
    // Fill in the form
    fireEvent.change(screen.getByPlaceholderText(/username/i), {
      target: { value: 'testuser' }
    })
    fireEvent.change(screen.getByPlaceholderText(/email address/i), {
      target: { value: 'test@example.com' }
    })
    fireEvent.change(screen.getByPlaceholderText(/password/i), {
      target: { value: 'password123' }
    })

    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: /sign up/i }))

    // Wait for the API call to complete
    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/signup',
        expect.objectContaining({
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          }
        })
      )

      // Check the request body separately to avoid order issues
      const requestBody = JSON.parse((global.fetch as jest.Mock).mock.calls[0][1].body)
      expect(requestBody).toEqual({
        username: 'testuser',
        email: 'test@example.com',
        password: 'password123'
      })
    })
  })

  it('handles signup error', async () => {
    // Mock failed API response
    ;(global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      json: () => Promise.resolve({
        detail: 'Email already registered'
      })
    })

    render(<SignUp />)
    
    // Fill in the form
    fireEvent.change(screen.getByPlaceholderText(/username/i), {
      target: { value: 'testuser' }
    })
    fireEvent.change(screen.getByPlaceholderText(/email address/i), {
      target: { value: 'test@example.com' }
    })
    fireEvent.change(screen.getByPlaceholderText(/password/i), {
      target: { value: 'password123' }
    })

    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: /sign up/i }))

    // Wait for the error message to appear
    await waitFor(() => {
      expect(screen.getByText(/email already registered/i)).toBeInTheDocument()
    })
  })
}) 